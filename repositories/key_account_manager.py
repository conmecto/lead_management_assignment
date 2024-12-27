from sqlalchemy.dialects.postgresql import insert
from models import KeyAccountManager
from .base import BaseRepository

class KeyAccountManagerRepository(BaseRepository):
    def create(self, kam_data: dict) -> KeyAccountManager:
        stmt = (
            insert(KeyAccountManager)
            .values(**kam_data)
            .returning(KeyAccountManager.id)
            .on_conflict_do_nothing(index_elements=['email'])
        )
        result = self.session.execute(stmt)
        row = result.fetchone()
        if not row:
            return None
        self.session.commit()
        kam_id = row[0]
        return kam_id

    def get_by_email(self, email: str) -> KeyAccountManager:
        return self.session.query(KeyAccountManager).filter_by(email=email).first()