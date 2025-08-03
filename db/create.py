from connect import connect
from models.base import Base

def create_db(engine):
    Base.metadata.create_all(engine)

engine = connect()
create_db(engine)
