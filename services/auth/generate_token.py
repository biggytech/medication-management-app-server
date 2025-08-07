import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

def generate_token(user):
    token = jwt.encode({
        'uuid': str(user.uuid),
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }, os.environ['JWT_SECRET_KEY'], algorithm="HS256")

    return token
