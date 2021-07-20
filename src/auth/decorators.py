from flask import g, request, current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from src.users.models import User
from flask_jwt_extended.exceptions import NoAuthorizationError
from functools import wraps

def load_current_user(func):

    @wraps(func)
    def load_user(*args, **kwargs):
        verify_jwt_in_request()
        jwt_identity = get_jwt_identity()
        user = User.query.get(jwt_identity["id"])
        if not user:
            current_app.logger.info("user not found from token")
            raise NoAuthorizationError("Invalid token, Unknown user")
        else:
            g.current_user = user
        return func(*args, **kwargs)

    return load_user
