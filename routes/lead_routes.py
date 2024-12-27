from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import LeadService, ContactService, AuthService, CallRecordService, PerformanceService
from schemas import LeadCreate, ContactCreate, CallRecordCreate, EndCallRecord
from config.database import db_instance

router = APIRouter()

verify_token = AuthService.verify_token

@router.post("/leads")
def create_lead(lead_data: LeadCreate, db: Session = Depends(db_instance.get_db), kam: dict = Depends(verify_token)):
    lead_service = LeadService(db)
    lead = lead_service.create_lead(kam["kam_id"], lead_data)
    return lead

@router.get("/leads")
def get_leads_requiring_calls(page: int = 1, per_page: int = 10, db: Session = Depends(db_instance.get_db), kam: dict = Depends(verify_token)):
    lead_service = LeadService(db)
    leads = lead_service.get_leads_requiring_calls(kam["kam_id"], page, per_page)
    return leads

@router.get("/leads/stats")
def get_leads_requiring_calls(db: Session = Depends(db_instance.get_db), kam: dict = Depends(verify_token)):
    performance_service = PerformanceService(db)
    leads_performance = performance_service.get_lead_stats(kam["kam_id"])
    return leads_performance

@router.get("/leads/{lead_id}")
def track_lead_status(lead_id: int, db: Session = Depends(db_instance.get_db), kam: dict = Depends(verify_token)):
    lead_service = LeadService(db)
    lead = lead_service.track_lead_status(kam["kam_id"], lead_id)
    return lead

@router.get("/leads/{lead_id}/order-patterns")
def get_leads_requiring_calls(lead_id: int, db: Session = Depends(db_instance.get_db), kam: dict = Depends(verify_token)):
    performance_service = PerformanceService(db)
    leads_performance = performance_service.get_order_patterns(lead_id)
    return leads_performance

@router.post("/leads/{lead_id}/contacts")
def create_contact(lead_id: int, contact_data: ContactCreate, db: Session = Depends(db_instance.get_db), kam: dict = Depends(AuthService.verify_token)):
    contact_service = ContactService(db)
    contact = contact_service.create_contact(kam["kam_id"], lead_id, contact_data)
    return contact

@router.post("/leads/{lead_id}/calls/start")
def create_call_record(lead_id: int, call_record_data: CallRecordCreate, db: Session = Depends(db_instance.get_db), kam: dict = Depends(AuthService.verify_token)):
    call_record_service = CallRecordService(db)
    call_record = call_record_service.start_call(kam["kam_id"], lead_id, call_record_data)
    return call_record

@router.get("/leads/{lead_id}/calls/latest")
def latest_call_record(lead_id: int, db: Session = Depends(db_instance.get_db), kam: dict = Depends(AuthService.verify_token)):
    call_record_service = CallRecordService(db)
    call_record = call_record_service.get_latest_call_record(lead_id)
    return call_record

@router.put("/leads/{lead_id}/calls/{call_record_id}/end")
def end_call_record(lead_id: int, call_record_id: int, end_call_data: EndCallRecord, db: Session = Depends(db_instance.get_db), kam: dict = Depends(AuthService.verify_token)):
    call_record_service = CallRecordService(db)
    call_record = call_record_service.end_call(kam["kam_id"], call_record_id, end_call_data)
    return call_record
    
