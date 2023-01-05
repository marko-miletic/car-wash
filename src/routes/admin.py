from flask import Blueprint, render_template, redirect, url_for, request

from src.logs import logger
from src.core.roles import ROLES
from src.core.roles import merged_login_role_required_decorator
from src.crud.user_operations import get_user_by_status, get_all_users
from src.crud.admin_operations import update_change_user_status
from src.crud.auth_operations import get_user_by_email, get_user_by_id
from src.crud.discount_operations import get_current_discount_data, post_create_new_discount
from src.models import Discount
from src.path_structure import TEMPLATES_DIRECTORY_PATH


admin = Blueprint('admin', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@admin.route('/', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def admin_index():
    try:
        admin_users = get_user_by_status(status='admin')
        print(admin_users)
        return render_template('admin_index.html',
                               admin_users=admin_users)
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('index.main'))


@admin.route('/update-user-status', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def admin_update_user_status_get():
    try:
        return render_template('admin_status.html')
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))


@admin.route('/update-user-status', methods=['POST'])
@merged_login_role_required_decorator(role_value='admin')
def admin_update_user_status_post():
    try:
        targeted_user = get_user_by_email(email=request.form.get('user_email'))
        if targeted_user.name == request.form.get('user_name'):
            update_change_user_status(new_role='admin', user_id=targeted_user.id)
        else:
            logger.logging.info('wrong input data')
        return redirect(url_for('admin.admin_index'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))


@admin.route('/update-discount-status', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def admin_update_discount_status_get():
    try:
        current_discount = get_current_discount_data()
        return render_template('admin_discount.html',
                               current_discount=current_discount)
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))


@admin.route('/update-discount-status', methods=['POST'])
@merged_login_role_required_decorator(role_value='admin')
def admin_update_discount_status_post():
    try:
        new_discount = Discount(base_discount=int(request.form.get('base_discount')),
                                additional_discount=int(request.form.get('additional_discount')),
                                additional_discount_description=str(request.form.get('additional_discount_desc')))
        post_create_new_discount(new_discount_object=new_discount)
        return redirect(url_for('admin.admin_update_discount_status_get'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_update_discount_status_get'))


@admin.route('/remove-additional-discount', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def admin_remove_additional_discount():
    try:
        current_discount = get_current_discount_data()
        new_discount = Discount(base_discount=current_discount.base_discount,
                                additional_discount=0,
                                additional_discount_description='-')
        post_create_new_discount(new_discount_object=new_discount)
        return redirect(url_for('admin.admin_update_discount_status_get'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_update_discount_status_get'))
