from sqlalchemy.orm import Session
from db.engine import engine

def with_session(subfunction, *args, **kwargs):
    with Session(engine) as session:
        return subfunction(session, *args, **kwargs)
