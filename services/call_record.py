import pytz
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models import CallRecord, Lead, Contact
from schemas import CallRecordCreate, EndCallRecord
from repositories import CallRecordRepository, LeadCallPlanRepository, LeadRepository, ContactRepository
from utils.enums import LeadStatus

class CallRecordService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.call_record_repo = CallRecordRepository(db_session)
        self.lead_repo = LeadRepository(db_session)
        self.contact_repo = ContactRepository(db_session)
        self.lead_call_plan_repo = LeadCallPlanRepository(db_session)

    def check_lost_lead_for_call(self, kam_id: int, lead_id: int) -> Lead:
        lead = self.lead_repo.get(kam_id, lead_id)
        if not lead or lead.status == LeadStatus.LOST:
            raise HTTPException(404, "Lead not found")
        return lead
    
    def check_contact_for_call(self, contact_id: int, lead_id: int) -> Contact:
        contact = self.contact_repo.get(contact_id)
        if not contact or contact.lead_id != lead_id:
            raise HTTPException(404, "Contact not found")
        return contact

    def start_call(self, kam_id: int, lead_id: int, call_record_data: CallRecordCreate) -> CallRecord:
        call_record_data_dict = call_record_data.model_dump()
        lead = self.check_lost_lead_for_call(kam_id, lead_id)
        self.check_contact_for_call(call_record_data_dict["contact_id"], lead_id)
        
        call_record_data_dict["kam_id"] = kam_id
        call_record_data_dict["lead_id"] = lead_id  
        call_record = self.call_record_repo.create(call_record_data_dict)
        self.lead_call_plan_repo.update_total_calls_today(lead_id)
        if lead.status == LeadStatus.NEW:
            self.lead_repo.update(lead_id, {"status": LeadStatus.NEGOTIATING})
        return {"call_record_id": call_record.id}

    def end_call(self, kam_id: int, call_record_id: int, end_call_data: EndCallRecord) -> CallRecord:
        end_call_data_dict = end_call_data.model_dump(exclude_unset=True)
        update_call_record = {"ended_at": datetime.now(pytz.UTC)}
        if "is_order_placed" in end_call_data_dict:
            update_call_record["is_order_placed"] = end_call_data_dict["is_order_placed"]
        if "order_value" in end_call_data_dict:
            update_call_record["order_value"] = end_call_data_dict["order_value"]
        call_record = self.call_record_repo.update(call_record_id, kam_id, update_call_record)
        if not call_record:
            raise HTTPException(404, "Call record not found")
        lead_id = call_record.lead_id
        lead = self.check_lost_lead_for_call(kam_id, lead_id)
        if "is_lead_lost" in end_call_data_dict and end_call_data_dict["is_lead_lost"]:
            self.lead_repo.update(lead_id, {"status": LeadStatus.LOST})
        elif end_call_data_dict["is_order_placed"] and lead.status == LeadStatus.NEGOTIATING:
            self.lead_repo.update(lead_id, {"status": LeadStatus.CONVERTED})
        return {"message": "Call ended successfully"}
    
    def get_latest_call_record(self, lead_id: int) -> CallRecord:
        call_record = self.call_record_repo.get_latest_call_record_by_lead_id(lead_id)
        if not call_record:
            raise HTTPException(404, "Call record not found")
        return call_record