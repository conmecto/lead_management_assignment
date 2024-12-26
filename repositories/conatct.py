from models.contact import Contact
from .base import BaseRepository

class ContactRepository(BaseRepository):    
    def create(self, contact_data: dict) -> Contact:
        contact = Contact(**contact_data)
        self.session.add(contact)
        self.session.commit()
        self.session.refresh(contact)
        return contact