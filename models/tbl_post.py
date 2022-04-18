from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import expression
from sqlalchemy.sql import func

# local imports
from utils.db_handler import handler




class TblPost(handler.Base):
    """
    SQL Alchemy Model for - Post
    """
    
    __tablename__ = "tbl_post"
    post_id = Column(
        Integer, nullable=False, primary_key=True, unique=True, autoincrement=True
    )
    user_id_fk = Column(Integer, ForeignKey("tbl_user.user_id"))
    title  = Column(String(256))
    description = Column(String(256))
    created_at = Column(TIMESTAMP, server_default=func.now())

    def to_json(self):
        return {
            "post_id": self.post_id,
            "user_id_fk": self.user_id_fk,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at.strftime('%d-%m-%Y'))
        }