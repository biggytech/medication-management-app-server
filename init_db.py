from db.scripts.add_delete_cascade import add_delete_cascade
from db.scripts.create_db_if_not_exists import create_db_if_not_exists
from db.scripts.create_db_tables import create_db_tables


def init_db():
    create_db_if_not_exists()
    create_db_tables()
    add_delete_cascade()


init_db()
