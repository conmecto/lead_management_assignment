from enum import Enum

class LeadStatus(Enum):
    NEW = "new"
    NEGOTIATING = "negotiating"
    CONVERTED = "converted"
    LOST = "lost"

class ContactRole(Enum):
    MANAGER = "manager"
    CHEF = "chef"
    OWNER = "owner"
    OTHER = "other"

class LeadType(Enum):
    RESTAURANT = "restaurant"