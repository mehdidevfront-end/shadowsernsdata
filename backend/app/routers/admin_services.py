from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db, Base, engine
from .. import models
from ..schemas import ServiceOut, ServiceApproveResponse

router = APIRouter(prefix="/api/services", tags=["services-admin"])

# Ensure tables exist
Base.metadata.create_all(bind=engine)

@router.get("/", response_model=List[ServiceOut])
def list_services(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = db.query(models.Service).order_by(models.Service.id.desc()).offset(offset).limit(limit).all()
    return items

@router.post("/{service_id}/approve", response_model=ServiceApproveResponse)
def approve_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.query(models.Service).get(service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    svc.approved = True
    db.add(svc)
    db.commit()
    return ServiceApproveResponse(id=svc.id, approved=svc.approved)
