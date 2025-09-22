from sqlalchemy import text
from services.db.decorators.with_session import with_session

@with_session
def drop_all_tables(session):
    session.execute(text("DROP SCHEMA public CASCADE;"))
    session.execute(text("CREATE SCHEMA public;"))
    session.commit()

drop_all_tables()
