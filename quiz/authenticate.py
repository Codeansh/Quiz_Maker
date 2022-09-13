from functools import wraps
import jwt
from flask import request
from quiz.users.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return 'Please Enter the token to verify your identity...'
        try:
            username = jwt.decode(token, 'This is a secret key', 'HS256')['username']
            current_user = User.objects(username=username).first()
            if not current_user:
                return 'Please login again....'

        except Exception as e:
            return {'Something went wrong ': str(e)}

        return f(current_user, *args, **kwargs)

    return decorated
