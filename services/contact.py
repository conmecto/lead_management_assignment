from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.contact import Contact
from schemas.contact import ContactCreate
from repositories.conatct import ContactRepository
from config.logger import logger

class ContactService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.contact_repo = ContactRepository(db_session)

    def create_contact(self, contact_data: ContactCreate, lead_id: int) -> Contact:
        try:
            contact_data_dict = contact_data.model_dump()
            contact_data_dict['lead_id'] = lead_id
            contact = self.contact_repo.create(contact_data_dict)
            return contact
        except IntegrityError as e:
            logger.error(f"Error creating contact: {str(e)}")
            raise HTTPException(status_code=404, detail="Lead not found")
    