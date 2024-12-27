import pytz
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.enums import ContactRole
from .base import Base

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(Enum(ContactRole), nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(pytz.UTC), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False)
    
    lead = relationship('Lead', back_populates='contacts')
    call_records = relationship('CallRecord', back_populates='contact')