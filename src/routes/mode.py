from flask import Blueprint, render_template, redirect, url_for, request

from src.logs import logger
from src.core.roles import merged_login_role_required_decorator
from src.models import Mode
from src.crud.mode_operations import post_create_new_mode, get_modes_by_active_status, update_change_mode_active_status
from src.path_structure import TEMPLATES_DIRECTORY_PATH


mode = Blueprint('mode', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@mode.route('/create', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def mode_create_get():
    try:
        return render_template('mode_create.html')
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))


@mode.route('/create', methods=['POST'])
@merged_login_role_required_decorator(role_value='admin')
def mode_create_post():
    try:
        new_mode = Mode(description=request.form.get('mode_description'),
                        price=int(request.form.get('mode_price')))
        post_create_new_mode(new_mode)
        return redirect(url_for('mode.mode_create_get'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('mode.mode_create_get'))


@mode.route('/active', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def mode_list_active():
    try:
        active_modes = get_modes_by_active_status(active_status=True)
        return render_template('mode_list.html',
                               modes=active_modes,
                               status_operation='Deactivate modes')
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))


@mode.route('/inactive', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def mode_list_inactive():
    try:
        inactive_modes = get_modes_by_active_status(active_status=False)
        return render_template('mode_list.html',
                               modes=inactive_modes,
                               status_operation='Activate modes')
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))


@mode.route('/change-status/<int:mode_id>/<int:status>', methods=['GET'])
@merged_login_role_required_decorator(role_value='admin')
def mode_change_status(mode_id: int, status: int):
    try:
        update_change_mode_active_status(new_status=bool(status), mode_id=mode_id)
        if status == 1:
            return redirect(url_for('mode.mode_list_inactive'))
        else:
            return redirect(url_for('mode.mode_list_active'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('admin.admin_index'))
