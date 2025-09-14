from functools import wraps
from flask import jsonify, request
from pydantic import ValidationError

BODY = 'json'

def validate_request(param, ValidationModel):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = getattr(request, param)

            try:
                ValidationModel(**data)
            except ValidationError as e:
                first_error = e.errors()[0]
                error_message = first_error['loc'][0] + ': ' + first_error['msg']
                return jsonify({'error': error_message}), 422

            return f(*args, **kwargs)

        return decorated

    return decorator
