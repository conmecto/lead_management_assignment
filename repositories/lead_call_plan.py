from sqlalchemy import select, func, desc
from datetime import datetime
from models.lead_call_plan import LeadCallPlan
from models.lead import Lead
from utils.enums import LeadStatus
from .base import BaseRepository

class LeadCallPlanRepository(BaseRepository):
    def create(self, lead_call_plan_data: dict) -> LeadCallPlan:
        lead_call_plan = LeadCallPlan(**lead_call_plan_data)
        self.session.add(lead_call_plan)
        return lead_call_plan
    
    def get_leads_by_call_frequency_days(self, kam_id: int, limit: int, offset: int) -> LeadCallPlan:
        query = (
            select(Lead.id, Lead.name, Lead.type, Lead.status, LeadCallPlan.last_call_at,
                   func.max(0, LeadCallPlan.daily_freq - LeadCallPlan.total_calls_today).label('pending_calls_today'))
            .outerjoin(LeadCallPlan, Lead.id == LeadCallPlan.lead_id)
            .where(Lead.kam_id == kam_id and Lead.status != LeadStatus.LOST and 'pending_calls_today' != 0)
            .order_by(desc('pending_calls_today'))
            .limit(limit)
            .offset(offset)
        )
        result = self.session.execute(query).fetchall()
        return result        
    
    def update_total_calls(self, lead_id: int) -> LeadCallPlan:
        lead_call_plan = self.session.query(LeadCallPlan).filter(LeadCallPlan.lead_id == lead_id).first()
        if not lead_call_plan:
            return None
        lead_call_plan.total_calls_today += 1
        lead_call_plan.last_call_at = datetime.now(datetime.timezone.utc)
        self.session.commit()
        return lead_call_plan