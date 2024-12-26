from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class BaseRepository(ABC):
    def __init__(self, session: Session):
        self.session = session