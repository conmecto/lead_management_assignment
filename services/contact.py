from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate
from repositories import ContactRepository, LeadRepository

class ContactService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.contact_repo = ContactRepository(db_session)
        self.lead_repo = LeadRepository(db_session)

    def create_contact(self, kam_id: int, lead_id: int, contact_data: ContactCreate) -> Contact:
        lead = self.lead_repo.get(kam_id, lead_id)
        if not lead:
            raise HTTPException(404, "Lead not found")
        contact_data_dict = contact_data.model_dump()
        contact_data_dict['lead_id'] = lead_id
        contact = self.contact_repo.create(contact_data_dict)
        return contact
    