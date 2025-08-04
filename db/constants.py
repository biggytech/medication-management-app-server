from sqlalchemy import URL
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URL = URL.create(
    os.environ['DB_DRIVER_NAME'],
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    host=os.environ['DB_HOST'],
    port=int(os.environ['DB_PORT']),
    database=os.environ['DB_DATABASE'],
)
