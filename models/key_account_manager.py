import pytz
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class KeyAccountManager(Base):
    __tablename__ = 'key_account_managers'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(pytz.UTC), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    leads = relationship('Lead', back_populates='key_account_manager')
    call_records = relationship('CallRecord', back_populates='key_account_manager')