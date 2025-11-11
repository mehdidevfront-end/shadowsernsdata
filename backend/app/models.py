from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, index=True, nullable=False)
    ip_address = Column(String, index=True, nullable=True)
    mac_address = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    events = relationship("DiscoveryEvent", back_populates="device")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    domain = Column(String, index=True, nullable=True)
    approved = Column(Boolean, default=False)
    risk_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    events = relationship("DiscoveryEvent", back_populates="service")

class DiscoveryEvent(Base):
    __tablename__ = "discovery_events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip = Column(String, index=True)
    mac = Column(String, index=True, nullable=True)
    domain = Column(String, index=True, nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    device = relationship("Device", back_populates="events")
    service = relationship("Service", back_populates="events")
    enrichment_status = Column(String, default="pending")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)
