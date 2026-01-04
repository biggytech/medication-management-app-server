from sqlalchemy import create_engine
from db.constants import DB_CONNECTION_URL, ROOT_DB_CONNECTION_URL


def connect():
    engine = create_engine(DB_CONNECTION_URL, echo=True)
    return engine


def root_connect():
    engine = create_engine(ROOT_DB_CONNECTION_URL, echo=True)
    return engine
