from functools import wraps
from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv

from models.user import User

load_dotenv()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # TODO: get from headers?
        token = request.cookies.get('jwt_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, os.environ['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
