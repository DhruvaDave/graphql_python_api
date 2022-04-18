"""
    DB Handler used across project
"""
import logging
from utils.db_utils import MySQLHandler
from config.db_config import DBConfig


logger = logging.getLogger("DB-Handler")

db_passcode = DBConfig.password.replace("%", "%%")
handler = MySQLHandler(
    DBConfig.host,
    DBConfig.user,
    DBConfig.password,
    DBConfig.port,
    DBConfig.dbname,
    DBConfig.pool_size,
)

def register_models():
    """
    Model initialization
    """
    logger.info("Initializing MySQL handler ... ")
    handler.initialize_db()

    from models.tbl_post import TblPost
    from models.tbl_user import TblUser


    handler.Base.metadata.create_all(bind=handler.engine)
