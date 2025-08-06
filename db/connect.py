from sqlalchemy import create_engine
from db.constants import DB_CONNECTION_URL

def connect():
    engine = create_engine(DB_CONNECTION_URL, echo=True)
    return engine
