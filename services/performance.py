from sqlalchemy.orm import Session
from repositories import CallRecordRepository, LeadRepository

class PerformanceService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.call_record_repo = CallRecordRepository(db_session)
        self.lead_repo = LeadRepository(db_session)

    def get_lead_stats(self, kam_id: int):
        temp = self.lead_repo.get_lead_stats(kam_id)
        return temp
    
    def get_order_patterns(self, lead_id: int):
        return self.call_record_repo.get_call_record_stats(lead_id)