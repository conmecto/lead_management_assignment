import pytz
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.enums import LeadStatus, LeadType
from .base import Base

class Lead(Base):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(LeadType), default=LeadType.RESTAURANT, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    created_at = Column(DateTime, default=datetime.now(pytz.UTC), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    kam_id = Column(Integer, ForeignKey('key_account_managers.id'), nullable=False)
    
    key_account_manager = relationship('KeyAccountManager', back_populates='leads')
    contacts = relationship('Contact', back_populates='lead')
    call_records = relationship('CallRecord', back_populates='lead')
    call_plan = relationship("LeadCallPlan", back_populates="lead", uselist=False)