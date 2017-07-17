from flask import request
from functools import wraps

from bulletin.common import errors
from bulletin.models.user import User
from bulletin.libs import jwttoken


def _get_auth_user():
    authorization = request.headers.get('Authorization')
    if authorization is None:
        return None
    if not authorization.startswith('Bearer '):
        return None
    token = jwttoken.decode(authorization[len('Bearer '):])
    if token is None or token.get('sub') is None:
        return None
    user = User.query.get(token.get('sub'))
    return user


def requires_auth():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = _get_auth_user()
            if user is None:
                raise errors.Unauthorized()
            kwargs['user'] = user
            return f(*args, **kwargs)
        return wrapped
    return wrapper
