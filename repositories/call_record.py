from sqlalchemy import func, case, extract
from models import CallRecord
from utils.helpers import get_day_of_week
from .base import BaseRepository

class CallRecordRepository(BaseRepository):    
    def create(self, call_record_data: dict) -> CallRecord:
        call_record = CallRecord(**call_record_data)
        self.session.add(call_record)
        self.session.commit()
        self.session.refresh(call_record)
        return call_record

    def update(self, call_record_id: int, kam_id: int, update_data: dict) -> CallRecord:
        call_record = self.session.query(CallRecord).filter(CallRecord.id == call_record_id and CallRecord.kam_id == kam_id).first()
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
        top_day_of_week = func.mode().within_group(
            case(
                (CallRecord.is_order_placed.is_(True), extract('dow', CallRecord.created_at))
            )
        ).label('top_day_of_week')
        top_date_of_month = func.mode().within_group(
            case(
                (CallRecord.is_order_placed.is_(True), extract('day', CallRecord.created_at))
            )
        ).label('top_date_of_month')
        query = (
            self.session.query(
                CallRecord.lead_id,
                func.count('*').label('order_placed_count'),
                top_day_of_week,
                top_date_of_month
            )
            .filter(
                CallRecord.lead_id == lead_id,
                CallRecord.is_order_placed.is_(True)
            )
            .group_by(CallRecord.lead_id)
        )
        result = query.first()
        if not result:
            return {
                "lead_id": lead_id,
                "order_placed_count": 0,
                "top_day_of_week": None,
                "top_date_of_month": None
            }
        order_patterns = {   
            "lead_id": result[0],
            "order_placed_count": result[1],
            "top_day_of_week": get_day_of_week(int(result[2])-1),
            "top_date_of_month": result[3]
        }
        return order_patterns