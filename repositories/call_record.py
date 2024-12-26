from sqlalchemy.orm import aliased
from sqlalchemy import func, case, extract
from models.call_record import CallRecord
from .base import BaseRepository

class CallRecordRepository(BaseRepository):    
    def create(self, call_record_data: dict) -> CallRecord:
        call_record = CallRecord(**call_record_data)
        self.session.add(call_record)
        self.session.commit()
        return call_record

    def update(self, call_record_id: int, update_data: dict) -> CallRecord:
        call_record = self.session.query(CallRecord).filter(CallRecord.id == call_record_id).first()
        for key, value in update_data.items():
            setattr(call_record, key, value)
        self.session.commit()
        self.session.refresh(call_record)
        return call_record
    
    def get_latest_call_record_by_lead_id(self, lead_id: int) -> CallRecord:
        call_record = (
            self.session.query(CallRecord).filter(CallRecord.lead_id == lead_id)
            .order_by(CallRecord.created_at.desc()).first()
        )
        return call_record
    
    def get_call_record_stats(self, lead_id: int):
        CallRecordAlias = aliased(CallRecord)
        
        order_placed_count = func.count(case([(CallRecordAlias.is_order_placed == True, 1)])).label('order_placed_count')
        call_record_count = func.count(CallRecordAlias.id).label('call_record_count')
        
        top_day_of_week = (
            func.mode().within_group(extract('dow', CallRecordAlias.created_at))
            .filter(CallRecordAlias.is_order_placed == True).label('top_day_of_week')
        )
        top_date_of_month = (
            func.mode().within_group(extract('day', CallRecordAlias.created_at))
            .filter(CallRecordAlias.is_order_placed == True).label('top_date_of_month')
        )
        query = (
            self.session.query(
                CallRecord.lead_id,
                order_placed_count,
                call_record_count,
                top_day_of_week,
                top_date_of_month
            )
            .filter(CallRecord.lead_id == lead_id)
            .group_by(CallRecord.lead_id)
        )
        return query.first()