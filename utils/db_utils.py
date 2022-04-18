"""
    Database Utils
"""

import logging
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config.db_config import DBConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySQLHandler:
    """
    MySQL handler for db query
    """

    def __init__(
        self,
        host,
        user,
        password,
        port=DBConfig.port,
        dbname="",
        pool_size=DBConfig.pool_size,
    ):
        self.host = host
        self.__user = user
        self.__password = password
        self.port = int(port)
        self.dbname = dbname
        self.pool_size = int(pool_size)
        self.url = None
        self._validate_credentials()
        self._create_engine()

    def _validate_credentials(self):
        if self.host is None:
            raise ValueError("No host specified for MySQL")
        if self.__user is None:
            raise ValueError("No user specified for MySQL")
        if self.__password is None:
            raise ValueError("No password specified for MySQL")
        if self.dbname is None or self.dbname == "":
            raise ValueError("No db specified for MySQL")

    def get_connection_string(self):
        if DBConfig.verify_ssl_cert:
            absolute_path = pathlib.Path(__file__).parent.parent.absolute()
            static_path = str(absolute_path) +\
                "/common_lib/cert/BaltimoreCyberTrustRoot.crt.pem"
            ssl_args = f"?ssl_ca={static_path}"
            logger.info("Connecting DB with SSL Certificate Verification")
        else:
            logger.info("Connecting DB without SSL Certificate Verification")
            ssl_args = "?ssl_verify_cert=false"
        self.url = (
            "mysql+pymysql://"
            + self.__user
            + ":"
            + self.__password
            + "@"
            + self.host
            + ":"
            + str(self.port)
            + "/"
            + self.dbname
            + ssl_args
        )
        return self.url

    def _create_engine(self):
        self.get_connection_string()

        self.engine = create_engine(
            self.url, pool_size=self.pool_size, pool_pre_ping=True, pool_recycle=300, echo=False,
            isolation_level="READ UNCOMMITTED")
        self.db_session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        # pylint: disable=C0103
        # note: Ignoring C0103: Attribute name as it's a modeling class
        self.Base = declarative_base(bind=self.engine)
        self.Base.query = self.db_session.query_property()

    def initialize_db(self):
        """
        Create db if not exists
        """
        if not database_exists(self.engine.url):
            # pylint: disable=E1101
            # Note: Disabled no-member as engine is a instance of sqlalchemy
            create_database(self.engine.url)
        else:
            # Connect the database if exists.
            self.engine.connect()

