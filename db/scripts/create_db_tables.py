from db.connect import connect
from models.base import Base
from models.all import all_models  # load all models so they update Base metadata


def create_db_tables():
    engine = connect()
    Base.metadata.create_all(engine)
