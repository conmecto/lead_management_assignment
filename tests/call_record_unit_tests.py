import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime
from models import Lead, Contact, CallRecord
from schemas import CallRecordCreate, EndCallRecord
from utils.enums import LeadStatus
from services import CallRecordService


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def call_record_service(mock_db_session):
    return CallRecordService(mock_db_session)


@pytest.fixture
def mock_lead():
    lead = MagicMock(spec=Lead)
    lead.id = 1
    lead.status = LeadStatus.NEW
    return lead


@pytest.fixture
def mock_contact():
    contact = MagicMock(spec=Contact)
    contact.id = 1
    contact.lead_id = 1
    return contact


@pytest.fixture
def mock_call_record():
    call_record = MagicMock(spec=CallRecord)
    call_record.id = 1
    call_record.lead_id = 1
    call_record.kam_id = 1
    return call_record


def test_check_lost_lead_for_call(call_record_service, mock_lead):
    # Mocking the lead repository call
    call_record_service.lead_repo.get.return_value = mock_lead

    # Test: Checking if lead is returned correctly
    result = call_record_service.check_lost_lead_for_call(1, 1)
    assert result == mock_lead, f"Expected lead: {mock_lead}, but got: {result}"
    call_record_service.lead_repo.get.assert_called_once_with(1, 1)

    # Test: Lead not found, should raise HTTPException
    call_record_service.lead_repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        call_record_service.check_lost_lead_for_call(1, 1)
    assert exc.value.status_code == 404, f"Expected status code 404, but got {exc.value.status_code}"


def test_start_call(call_record_service, mock_lead, mock_contact, mock_call_record):
    # Mocking the repositories
    call_record_service.lead_repo.get.return_value = mock_lead
    call_record_service.contact_repo.get.return_value = mock_contact
    call_record_service.call_record_repo.create.return_value = mock_call_record
    call_record_service.lead_call_plan_repo.update_total_calls_today.return_value = None
    call_record_service.lead_repo.update.return_value = None

    call_record_data = CallRecordCreate(contact_id=1)

    # Test: Start Call - Call record should be created, and lead status should change
    result = call_record_service.start_call(1, 1, call_record_data)
    assert result == {"call_record_id": mock_call_record.id}, f"Expected call record id: {mock_call_record.id}, but got {result}"

    # Ensure the correct methods were called
    call_record_service.call_record_repo.create.assert_called_once_with({'contact_id': 1, 'kam_id': 1, 'lead_id': 1})
    call_record_service.lead_call_plan_repo.update_total_calls_today.assert_called_once_with(1)
    call_record_service.lead_repo.update.assert_called_once_with(1, {'status': LeadStatus.NEGOTIATING})

    # Test: Invalid Contact
    call_record_service.contact_repo.get.return_value = None
    with pytest.raises(HTTPException) as exc:
        call_record_service.start_call(1, 1, call_record_data)
    assert exc.value.status_code == 404, f"Expected status code 404, but got {exc.value.status_code}"


def test_end_call(call_record_service, mock_lead, mock_call_record):
    # Mocking repositories
    call_record_service.call_record_repo.update.return_value = mock_call_record
    call_record_service.lead_repo.get.return_value = mock_lead

    end_call_data = EndCallRecord(is_order_placed=True, order_value=100)

    # Test: End Call - Should return success and lead status should change
    result = call_record_service.end_call(1, 1, end_call_data)
    assert result == {"message": "Call ended successfully"}, f"Expected message: 'Call ended successfully', but got {result}"

    # Ensure that the lead status is updated correctly
    call_record_service.lead_repo.update.assert_called_once_with(1, {"status": LeadStatus.CONVERTED})

    # Test: Call record not found
    call_record_service.call_record_repo.update.return_value = None
    with pytest.raises(HTTPException) as exc:
        call_record_service.end_call(1, 1, end_call_data)
    assert exc.value.status_code == 404, f"Expected status code 404, but got {exc.value.status_code}"


def test_get_latest_call_record(call_record_service, mock_call_record):
    # Mocking the repository
    call_record_service.call_record_repo.get_latest_call_record_by_lead_id.return_value = mock_call_record

    # Test: Get Latest Call Record
    result = call_record_service.get_latest_call_record(1)
    assert result == mock_call_record, f"Expected: {mock_call_record}, but got: {result}"

    # Test: Call record not found
    call_record_service.call_record_repo.get_latest_call_record_by_lead_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        call_record_service.get_latest_call_record(1)
    assert exc.value.status_code == 404, f"Expected status code 404, but got {exc.value.status_code}"
