from sqlalchemy.orm import aliased
from sqlalchemy import func, case, cast, Float
from models.lead import Lead
from models.call_record import CallRecord
from utils.enums import LeadStatus
from .base import BaseRepository

class LeadRepository(BaseRepository):
    def create(self, lead_data: dict) -> Lead:
        lead = Lead(**lead_data)
        self.session.add(lead)
        return lead
    
    def get(self, lead_id: int) -> Lead:
        return self.session.query(Lead).filter(Lead.id == lead_id).first()
    
    def update(self, lead_id: int, update_data: dict) -> Lead:
        self.session.query(Lead).filter(Lead.id == lead_id).update(update_data)
        self.session.commit()
        return self.get(lead_id)
    
    def get_lead_stats(self, kam_id: int):
        CallRecordAlias = aliased(CallRecord)
        order_placed_count = func.count(case([(CallRecordAlias.is_order_placed == True, 1)])).label('order_placed_count')
        call_record_count = func.count(CallRecordAlias.id).label('call_record_count')
        ratio = (cast(order_placed_count, Float) / cast(call_record_count, Float) * 100).label('order_placed_ratio')
        avg_order_value = func.avg(CallRecordAlias.order_value).label('avg_order_value')
        performance = case(
            [
                ((ratio < 30) | (avg_order_value < 10000), 'bad')
            ],
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
        return query.all()