from connect import connect
from models.base import Base

def migrate(engine):
    Base.metadata.create_all(engine)

engine = connect()
migrate(engine)
