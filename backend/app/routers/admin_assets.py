from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db, Base, engine
from .. import models
from ..schemas import DeviceOut

router = APIRouter(prefix="/api/assets", tags=["assets-admin"])

# Ensure tables exist
Base.metadata.create_all(bind=engine)

@router.get("/", response_model=List[DeviceOut])
def list_assets(limit: int = 50, offset: int = 0, q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Device)
    if q:
        like = f"%{q}%"
        query = query.filter((models.Device.hostname.ilike(like)) | (models.Device.ip_address.ilike(like)))
    items = query.order_by(models.Device.id.desc()).offset(offset).limit(limit).all()
    return items
