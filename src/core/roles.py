from functools import wraps
from flask import redirect, url_for
from flask_login import current_user, login_required


# maps program passed string roles to required integer database values
# program uses string named values for better code understanding
ROLES = {
    'admin': 1,
    'user': 0
}


def role_required(role_value: int, redirect_endpoint: str = 'auth.login'):
    """
    function:
        Checks for user role value and gives access to user if role value is higher than
        required value for accessing requested route.
        If user is not logged in then access is denied.
    parameters:
        role_value: int - value required for accessing requested route
        redirect_endpoint: str - route used in case that user is denied access to given route
    """
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if not hasattr(current_user, 'role') or current_user.role < role_value:
                return redirect(url_for(redirect_endpoint))
            return func(*args, **kwargs)
        return authorize
    return decorator


def role_names(role: str) -> int:
    return ROLES.get(role, 0)


def merged_login_role_required_decorator(role_value: str, redirect_endpoint: str = 'auth.login'):
    """
    function:
        Combines login_required and role_required decorators.
    parameters:
        role_value: int - value required for accessing requested route
        redirect_endpoint: str - route used in case that user is denied access to given route
    """

    # pass the arguments to the decorator factories and
    # obtain the actual decorators
    role_decorator = role_required(role_value=role_names(role=role_value), redirect_endpoint=redirect_endpoint)

    # create a function decorator that applies the two
    # decorators that are just created
    def real_decorator(func):
        return role_decorator(login_required(func))
    return real_decorator
