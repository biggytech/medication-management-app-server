from connect import connect

from models.base import Base
from models.all import all_models # load all models so they update Base metadata

def create_db(engine):
    Base.metadata.create_all(engine)

engine = connect()
create_db(engine)
