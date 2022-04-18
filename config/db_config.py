"""
    Config related to db
"""
import ast
from os import environ
import logging

logger = logging.getLogger("DB-Config")


class DBConfig:
    """
    Database configuration
    """

    # host = environ.get("DB_HOST")
    # port = environ.get("DB_PORT", 3306)
    # user = environ.get("DB_USER")
    # password = environ.get("DB_PASSWORD")
    # charset = environ.get("DB_CHARSET", "utf8")
    # dbname = environ.get("DB_NAME")

    host = "localhost"
    port = 3306
    user = "root"
    password = "root"
    charset = "utf8"
    dbname = "graphql_demo"
    pool_size = 5
    verify_ssl_cert = ast.literal_eval(environ.get("VERIFY_SSL_CERT", "False"))

    if host is None:
        logger.info(f"Database Host is not found")
    if user is None:
        logger.info(f"Database User is not found")
    if password is None:
        logger.info(f"Database Password is not found")
