import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Lead
from repositories import LeadRepository, LeadCallPlanRepository
from schemas import LeadCreate
from config.logger import logger
from services import LeadService

def test_create_lead_success():
    db_session = MagicMock(spec=Session)
    lead_repo = MagicMock(spec=LeadRepository)
    lead_call_plan_repo = MagicMock(spec=LeadCallPlanRepository)
    db_session.begin = MagicMock()
    db_session.rollback = MagicMock()

    lead_data = LeadCreate(name="Test Lead", email="test@example.com")
    lead = MagicMock(spec=Lead, id=1)
    lead_repo.create.return_value = lead

    lead_call_plan = MagicMock()
    lead_call_plan_repo.create.return_value = lead_call_plan

    service = LeadService(db_session)
    service.lead_repo = lead_repo
    service.lead_call_plan_repo = lead_call_plan_repo

    result = service.create_lead(kam_id=123, lead=lead_data)

    assert result == {"lead_id": lead.id}
    lead_repo.create.assert_called_once_with({"name": "Test Lead", "email": "test@example.com", "kam_id": 123})
    lead_call_plan_repo.create.assert_called_once_with({"lead_id": lead.id, "daily_freq": 5})

def test_create_lead_failure():
    db_session = MagicMock(spec=Session)
    lead_repo = MagicMock(spec=LeadRepository)
    lead_call_plan_repo = MagicMock(spec=LeadCallPlanRepository)
    db_session.begin = MagicMock()
    db_session.rollback = MagicMock()

    lead_data = LeadCreate(name="Test Lead", email="test@example.com")
    lead_repo.create.return_value = None

    service = LeadService(db_session)
    service.lead_repo = lead_repo
    service.lead_call_plan_repo = lead_call_plan_repo

    with pytest.raises(HTTPException) as excinfo:
        service.create_lead(kam_id=123, lead=lead_data)

    assert excinfo.value.status_code == 500
    assert "Internal Server Error" in str(excinfo.value.detail)
    db_session.rollback.assert_called_once()
    logger.error.assert_called_once()

def test_track_lead_status_success():
    db_session = MagicMock(spec=Session)
    lead_repo = MagicMock(spec=LeadRepository)
    lead = MagicMock(spec=Lead)

    lead_repo.get.return_value = lead

    service = LeadService(db_session)
    service.lead_repo = lead_repo

    result = service.track_lead_status(kam_id=123, lead_id=1)

    assert result == lead
    lead_repo.get.assert_called_once_with(123, 1)

def test_track_lead_status_not_found():
    db_session = MagicMock(spec=Session)
    lead_repo = MagicMock(spec=LeadRepository)
    lead_repo.get.return_value = None

    service = LeadService(db_session)
    service.lead_repo = lead_repo

    with pytest.raises(HTTPException) as excinfo:
        service.track_lead_status(kam_id=123, lead_id=1)

    assert excinfo.value.status_code == 404
    assert "Lead not found" in str(excinfo.value.detail)
    lead_repo.get.assert_called_once_with(123, 1)

def test_get_leads_requiring_calls():
    db_session = MagicMock(spec=Session)
    lead_repo = MagicMock(spec=LeadRepository)
    leads = [MagicMock(spec=Lead), MagicMock(spec=Lead)]

    lead_repo.get_leads_by_call_frequency_days.return_value = leads

    service = LeadService(db_session)
    service.lead_repo = lead_repo

    result = service.get_leads_requiring_calls(kam_id=123, page=2, per_page=10)

    assert result == leads
    lead_repo.get_leads_by_call_frequency_days.assert_called_once_with(123, limit=10, offset=10)