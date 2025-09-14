from sqlalchemy.orm import Session
from db.engine import engine

# TODO: convert to decorator
def with_session(subfunction, *args, **kwargs):
    with Session(engine) as session:
        return subfunction(session, *args, **kwargs)
