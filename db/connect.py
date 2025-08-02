from sqlalchemy import create_engine
from sqlalchemy import URL

def connect():
    # TODO: use env variables for DB connection params
    url_object = URL.create(
        "postgresql+psycopg2",
        username="postgres",
        password="postgres",
        host="localhost",
        port=5432,
        database="medication_test",
    )
    engine = create_engine(url_object, echo=True)
    return engine
