from functools import wraps
from flask import redirect, url_for
from flask_login import current_user, login_required


ROLES = {
    'admin': 1,
    'user': 0
}


def role_required(role_value: int, redirect_endpoint: str = 'auth.login'):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if current_user.role < role_value:
                return redirect(url_for(redirect_endpoint))
            return func(*args, **kwargs)
        return authorize
    return decorator


def role_names(role: str) -> int:
    return ROLES.get(role, 0)


def merged_login_role_required_decorator(role_value: str, redirect_endpoint: str = 'auth.login'):
    # pass the arguments to the decorator factories and
    # obtain the actual decorators
    role_decorator = role_required(role_value=role_names(role=role_value), redirect_endpoint=redirect_endpoint)
    # create a function decorator that applies the two
    # decorators we just created

    def real_decorator(func):
        return role_decorator(login_required(func))
    return real_decorator
