import pytz
from datetime import datetime
from models import LeadCallPlan
from .base import BaseRepository

class LeadCallPlanRepository(BaseRepository):
    def create(self, lead_call_plan_data: dict) -> LeadCallPlan:
        lead_call_plan = LeadCallPlan(**lead_call_plan_data)
        self.session.add(lead_call_plan)
        return lead_call_plan
    
    def update_total_calls_today(self, lead_id: int) -> LeadCallPlan:
        lead_call_plan = self.session.query(LeadCallPlan).filter(LeadCallPlan.lead_id == lead_id).first()
        if not lead_call_plan:
            return None
        lead_call_plan.total_calls_today += 1
        lead_call_plan.last_call_at = datetime.now(pytz.UTC)
        self.session.commit()
        self.session.refresh(lead_call_plan)
        return lead_call_plan