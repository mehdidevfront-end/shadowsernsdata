from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from ..db import get_db, Base, engine
from .. import models
from ..schemas import IngestEvent, IngestResponse, DiscoveryEventOut

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

# Ensure tables exist (idempotent)
Base.metadata.create_all(bind=engine)

SERVICE_CATALOG = {
    "drive.google.com": {"name": "Google Drive", "risk_score": 70},
    "dropbox.com": {"name": "Dropbox", "risk_score": 60},
    "slack.com": {"name": "Slack", "risk_score": 50},
}


def resolve_service(domain: str, db: Session):
    if not domain:
        return None
    # Try to find by domain
    svc = db.query(models.Service).filter(models.Service.domain == domain).first()
    if svc:
        return svc
    # Try to seed from catalog
    for key, meta in SERVICE_CATALOG.items():
        if domain.endswith(key):
            svc = models.Service(name=meta["name"], domain=domain, risk_score=meta["risk_score"], approved=False)
            db.add(svc)
            db.commit()
            db.refresh(svc)
            return svc
    # Fallback: create unknown service entry
    svc = models.Service(name=domain, domain=domain, risk_score=20, approved=False)
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc


@router.post("/events", response_model=IngestResponse)
def ingest_events(items: List[IngestEvent], db: Session = Depends(get_db)):
    received = len(items)
    stored = 0
    for it in items:
        # Device: find or create by MAC then IP
        device = None
        if it.mac:
            device = db.query(models.Device).filter(models.Device.mac_address == it.mac).first()
        if not device and it.ip:
            device = db.query(models.Device).filter(models.Device.ip_address == it.ip).first()
        if not device:
            device = models.Device(hostname=it.hostname or "unknown", ip_address=it.ip, mac_address=it.mac)
            db.add(device)
            db.commit()
            db.refresh(device)
        else:
            # Update hostname/ip if newly known
            if it.hostname and device.hostname != it.hostname:
                device.hostname = it.hostname
            if it.ip and device.ip_address != it.ip:
                device.ip_address = it.ip
            db.add(device)
            db.commit()

        svc = resolve_service(it.domain, db) if it.domain else None

        evt = models.DiscoveryEvent(
            timestamp=it.timestamp or datetime.now(timezone.utc),
            ip=it.ip,
            mac=it.mac,
            domain=it.domain,
            device_id=device.id if device else None,
            service_id=svc.id if svc else None,
            enrichment_status="done" if svc else "pending",
        )
        db.add(evt)
        stored += 1
    db.commit()
    return IngestResponse(received=received, stored=stored)


@router.get("/events", response_model=List[DiscoveryEventOut])
def list_events(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    q = db.query(models.DiscoveryEvent).order_by(models.DiscoveryEvent.id.desc()).offset(offset).limit(limit)
    return q.all()
