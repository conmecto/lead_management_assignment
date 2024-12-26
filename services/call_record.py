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

class CallRecordService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.call_record_repo = CallRecordRepository(db_session)
        self.lead_repo = LeadRepository(db_session)
        self.lead_call_plan_repo = LeadCallPlanRepository(db_session)

    def start_call(self, call_record_data: CallRecordCreate) -> CallRecord:
        call_record_data_dict = call_record_data.model_dump()
        lead_id = call_record_data_dict["lead_id"]
        lead = self.lead_repo.get(lead_id)
        if not lead or lead.status == LeadStatus.LOST:
            raise HTTPException(status_code=404, detail="Lead not found")
        try:
            with self.db_session.begin():
                lead_call_plan = self.lead_call_plan_repo.update_total_calls(lead_id)
                if not lead_call_plan:
                    raise ValueError("Call plan update failed")
                call_record = self.call_record_repo.create(call_record_data_dict)
                if not call_record:
                    raise ValueError("Call record creation failed")
                if lead.status == LeadStatus.NEW:
                    self.lead_repo.update(lead_id, {"status": LeadStatus.NEGOTIATING})
                return call_record
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error creating call record: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def end_call(self, call_record_id: int, end_call_data: EndCallRecord) -> CallRecord:
        end_call_data_dict = end_call_data.model_dump(exclude_unset=True)
        update_call_record = {
            "ended_at": datetime.now(datetime.timezone.utc),
            "is_order_placed": end_call_data_dict["is_order_placed"]
        }
        if end_call_data_dict["order_value"]:
            update_call_record["order_value"] = end_call_data_dict["order_value"]
        call_record = self.call_record_repo.update(call_record_id, update_call_record)
        if not call_record:
            raise HTTPException(status_code=404, detail="Call record not found")
        lead_id = call_record["lead_id"]
        lead = self.lead_repo.get(lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        if end_call_data_dict["is_lead_lost"]:
            self.lead_repo.update(lead_id, {"status": LeadStatus.LOST})
        elif end_call_data_dict["is_order_placed"] and lead.status == LeadStatus.NEGOTIATING:
            self.lead_repo.update(lead_id, {"status": LeadStatus.CONVERTED})
        return call_record
    
    def get_latest_call_record(self, lead_id: int) -> CallRecord:
        call_record = self.call_record_repo.get_latest_call_record_by_lead_id(lead_id)
        if not call_record:
            raise HTTPException(status_code=404, detail="Call record not found")
        return call_record