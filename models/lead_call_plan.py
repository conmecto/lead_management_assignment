from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class LeadCallPlan(Base):
    __tablename__ = 'lead_call_plans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_freq = Column(Integer, nullable=False)
    last_call_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=True)
    total_calls_today = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), unique=True, nullable=False)
    
    lead = relationship("Lead", back_populates="call_plan")
