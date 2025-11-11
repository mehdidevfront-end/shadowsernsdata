from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import csv
import io

from ..db import get_db
from .. import models

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/export")
def export_report(db: Session = Depends(get_db)):
    # Simple CSV export combining services and devices counts
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["type", "id", "name_or_hostname", "extra1", "extra2"])

    for svc in db.query(models.Service).all():
        writer.writerow(["service", svc.id, svc.name, svc.domain or "", f"approved={svc.approved}"])

    for dev in db.query(models.Device).all():
        writer.writerow(["device", dev.id, dev.hostname, dev.ip_address or "", dev.mac_address or ""])

    output.seek(0)
    return StreamingResponse(iter([output.read()]), media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=report.csv"
    })
