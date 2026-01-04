from db.connect import root_connect
import os
from sqlalchemy import text
from sqlalchemy.orm import Session


def create_db_if_not_exists():
    engine = root_connect().execution_options(
        isolation_level="AUTOCOMMIT"
    )
    db_name = os.environ['DB_DATABASE']
    with Session(engine) as session:
        result = session.execute(text("SELECT FROM pg_database WHERE datname = '{db_name}'".format(db_name=db_name)))
        names = [row for row in result]
        print(names)
        if len(names) == 0:
            session.execute(
                text("CREATE DATABASE {db_name}".format(db_name=db_name))
            )
