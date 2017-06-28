from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def perimission_required(permission):
    def decorator(f):
        @wraps(f)
        def deorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return deorated_function
    return decorator


def admin_required(f):
    return perimission_required(Permission.ADMINISTER)(f)
