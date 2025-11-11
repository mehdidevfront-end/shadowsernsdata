from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class IngestEvent(BaseModel):
    ip: str
    mac: Optional[str] = None
    domain: Optional[str] = None
    hostname: Optional[str] = None
    timestamp: Optional[datetime] = None

class IngestResponse(BaseModel):
    received: int
    stored: int

class DiscoveryEventOut(BaseModel):
    id: int
    timestamp: datetime
    ip: str
    mac: Optional[str]
    domain: Optional[str]
    device_id: Optional[int]
    service_id: Optional[int]

    class Config:
        orm_mode = True

class DeviceOut(BaseModel):
    id: int
    hostname: str
    ip_address: Optional[str]
    mac_address: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class ServiceOut(BaseModel):
    id: int
    name: str
    domain: Optional[str]
    approved: bool
    risk_score: int
    created_at: datetime

    class Config:
        orm_mode = True

class ServiceApproveResponse(BaseModel):
    id: int
    approved: bool
