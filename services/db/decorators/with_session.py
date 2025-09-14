from functools import wraps
from sqlalchemy.orm import Session
from db.engine import engine

def with_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        with Session(engine) as session:
            return f(session, *args, **kwargs)

    return decorated
