from sqlalchemy.orm import aliased
from sqlalchemy import select, func, desc, case, cast, Float
from models import Lead, CallRecord, LeadCallPlan
from utils.enums import LeadStatus
from .base import BaseRepository

class LeadRepository(BaseRepository):
    def create(self, lead_data: dict) -> Lead:
        lead = Lead(**lead_data)
        self.session.add(lead)
        self.session.flush()
        return lead
    
    def get(self, kam_id, lead_id: int) -> Lead:
        lead = self.session.query(Lead).filter(Lead.id == lead_id and Lead.kam_id == kam_id).first()
        return lead
    
    def update(self, lead_id: int, update_data: dict):
        self.session.query(Lead).filter(Lead.id == lead_id).update(update_data)
        self.session.commit()
    
    def get_leads_by_call_frequency_days(self, kam_id: int, limit: int, offset: int) -> LeadCallPlan:
        query = (
            select(
                Lead.id, 
                Lead.name, 
                Lead.type, Lead.status, LeadCallPlan.last_call_at,
                   func.greatest(0, LeadCallPlan.daily_freq - LeadCallPlan.total_calls_today).label('pending_calls_today'))
            .outerjoin(LeadCallPlan, Lead.id == LeadCallPlan.lead_id)
            .where(Lead.kam_id == kam_id and Lead.status != LeadStatus.LOST and 'pending_calls_today' != 0)
            .order_by(desc('pending_calls_today'))
            .limit(limit)
            .offset(offset)
        )
        result = self.session.execute(query).all()
        formatted_result = [
            {
                "id": row.id,
                "name": row.name,
                "type": row.type,
                "status": row.status,
                "last_call_at": row.last_call_at,
                "pending_calls_today": row.pending_calls_today,
            }
            for row in result
        ]
        return formatted_result
    
    def get_lead_stats(self, kam_id: int):
        CallRecordAlias = aliased(CallRecord)
        order_placed_count = func.count(case((CallRecordAlias.is_order_placed == True, 1))).label('order_placed_count')
        call_record_count = func.count(CallRecordAlias.id).label('call_record_count')
        ratio = (cast(order_placed_count, Float) / cast(call_record_count, Float) * 100).label('order_placed_ratio')
        avg_order_value = func.avg(CallRecordAlias.order_value).label('avg_order_value')
        performance = case(
            ((ratio < 30) | (avg_order_value < 10000), 'bad'),
            else_='good'
        ).label('performance')

        query = (
            self.session.query(
                Lead.id.label('lead_id'),
                Lead.status,
                order_placed_count,
                call_record_count,
                ratio,
                avg_order_value,
                performance
            )
            .outerjoin(CallRecordAlias, Lead.id == CallRecordAlias.lead_id)
            .filter(
                Lead.kam_id == kam_id,
                Lead.status.in_([LeadStatus.NEGOTIATING, LeadStatus.CONVERTED])
            )
            .group_by(Lead.id, Lead.status)
            .order_by(avg_order_value)
        )
        result = query.all()
        formatted_result = [
            {
                "lead_id": row.lead_id,
                "status": row.status,
                "order_placed_count": row.order_placed_count,
                "call_record_count": row.call_record_count,
                "order_placed_ratio": row.order_placed_ratio,
                "avg_order_value": row.avg_order_value,
                "performance": row.performance,
            }
            for row in result
        ]
        return formatted_result