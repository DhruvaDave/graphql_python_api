from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import expression
from sqlalchemy.sql import func

# local imports
from utils.db_handler import handler




class TblUser(handler.Base):
    """
    SQL Alchemy Model for - User
    """
    
    __tablename__ = "tbl_user"
    user_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    first_name  = Column(String(256))
    last_name = Column(String(256))
    created_at = Column(TIMESTAMP, server_default=func.now())

    def to_json(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": str(self.created_at.strftime('%d-%m-%Y'))
        }