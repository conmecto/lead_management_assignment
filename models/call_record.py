import pytz
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date, Time, Numeric, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class CallRecord(Base):
    __tablename__ = 'call_records'
    
    id = Column(Integer, primary_key=True, index=True)
    is_order_placed = Column(Boolean, default=False, nullable=False)
    order_value = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.now(pytz.UTC), nullable=False)
    ended_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    kam_id = Column(Integer, ForeignKey('key_account_managers.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False)
    
    key_account_manager = relationship('KeyAccountManager', back_populates='call_records')
    lead = relationship('Lead', back_populates='call_records')
    contact = relationship('Contact', back_populates='call_records')