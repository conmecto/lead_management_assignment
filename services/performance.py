from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models.call_record import CallRecord
from schemas.call_record import CallRecordCreate, EndCallRecord
from repositories.call_record import CallRecordRepository
from repositories.lead_call_plan import LeadCallPlanRepository
from repositories.lead import LeadRepository
from utils.enums import LeadStatus
from config.logger import logger

class PerformanceService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.call_record_repo = CallRecordRepository(db_session)
        self.lead_repo = LeadRepository(db_session)

    def get_lead_stats(self, kam_id: int):
        return self.lead_repo.get_lead_stats(kam_id)
    
    def get_ordering_pattern(self, lead_id: int):
        return self.call_record_repo.get_call_record_stats(lead_id)