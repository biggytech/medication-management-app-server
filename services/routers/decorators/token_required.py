import os
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import request, jsonify

from models.user.operations.get_user_by_uuid import get_user_by_uuid

load_dotenv()

PREFIX = 'Bearer '


def normalize_token(header):
    if not header.startswith(PREFIX):
        raise ValueError('Invalid token')

    return header[len(PREFIX):]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            normalized_token = normalize_token(token)
            data = jwt.decode(normalized_token, os.environ['JWT_SECRET_KEY'], algorithms=["HS256"])
            user = get_user_by_uuid(data['uuid'])
        except:
            return jsonify({'error': 'Token is invalid!'}), 401

        return f(user, *args, **kwargs)

    return decorated
