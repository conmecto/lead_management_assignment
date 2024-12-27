from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Lead
from repositories import LeadRepository, LeadCallPlanRepository
from schemas import LeadCreate
from config.logger import logger

class LeadService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.lead_repo = LeadRepository(db_session)
        self.lead_call_plan_repo = LeadCallPlanRepository(db_session)

    def create_lead(self, kam_id: int, lead: LeadCreate) -> Lead:
        try:
            with self.db_session.begin():
                lead_dict = lead.model_dump()
                lead_dict["kam_id"] = kam_id
                lead = self.lead_repo.create(lead_dict)
                if not lead:
                    raise ValueError("Lead creation failed")
                lead_call_plan_data = {
                    "lead_id": lead.id,
                    "daily_freq": 5
                }
                lead_call_plan = self.lead_call_plan_repo.create(lead_call_plan_data)
                if not lead_call_plan:
                    raise ValueError("Lead call plan creation failed")
                return {
                    "lead_id": lead.id
                }
        except Exception as e:
            self.db_session.rollback()
            logger.error("Error creating lead: %s", str(e), stack_info=True)
            raise HTTPException(500, "Internal Server Error")

    def track_lead_status(self, kam_id: int, lead_id: int) -> Lead:
        lead = self.lead_repo.get(kam_id, lead_id)
        if not lead:
            raise HTTPException(404, "Lead not found")
        return lead
    
    def get_leads_requiring_calls(self, kam_id: int, page: int, per_page: int):
        offset = (page - 1) * per_page
        leads = self.lead_repo.get_leads_by_call_frequency_days(kam_id, limit=per_page, offset=offset)
        return leads