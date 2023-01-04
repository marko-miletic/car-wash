from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.logs import logger
from src.models import User
from src.crud import auth_operations
from src.core.roles import merged_login_role_required_decorator
from src.path_structure import TEMPLATES_DIRECTORY_PATH


auth = Blueprint('auth', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = auth_operations.get_user_by_email(email)
        logger.logging.info(user)

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            raise ValueError('Wrong credentials input')

        login_user(user, remember=remember)
        return redirect(url_for('index.profile'))

    except ValueError as err:
        logger.logging.error(err)
        return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        car_registration = request.form.get('car_registration')

        user = auth_operations.get_user_by_email(email)
        logger.logging.info(user)

        if user:
            flash('Email address already exists')
            raise ValueError('email already exists')

        new_user_object = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='sha256'),
            car_registration=car_registration
        )
        # add the new user to the database
        auth_operations.post_create_new_user(new_user_object)

        return redirect(url_for('auth.login'))

    except ValueError as err:
        logger.logging.error(err)
        return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.main'))


@auth.route('admin-test')
@merged_login_role_required_decorator(role_value='admin')
def admin_test():
    return make_response({'status': 200, 'role': current_user.role})
