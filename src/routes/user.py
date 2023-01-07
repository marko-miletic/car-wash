from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from src.logs import logger
from src.core.roles import ROLES
from src.crud.auth_operations import get_user_by_id
from src.crud.program_operations import post_mode_in_program, delete_mode_from_program
from src.crud.invoice_operations import post_create_new_invoice, get_split_user_invoices
from src.utility.user_program import get_user_selected_and_available_modes
from src.utility.invoice_calculation import calculate_program_invoice_price
from src.models import Invoice
from src.path_structure import TEMPLATES_DIRECTORY_PATH


user = Blueprint('user', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@user.route('/', methods=['GET'])
@user.route('/profile', methods=['GET'])
@login_required
def user_profile():
    try:
        user_data = get_user_by_id(user_id=current_user.id)
        user_role_mapper = {value: key for key, value in ROLES.items()}
        user_split_by_five_invoices = get_split_user_invoices(user_id=current_user.id, split_number=5)
        return render_template('user_profile.html',
                               user=user_data,
                               role_mapper=user_role_mapper,
                               user_invoices_first_part=user_split_by_five_invoices[0],
                               user_invoices_rest=user_split_by_five_invoices[1])
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('index.main'))


@user.route('/program', methods=['GET'])
@login_required
def user_program():
    try:
        selected_unselected_modes = get_user_selected_and_available_modes(user_id=current_user.id)
        price_with_discount = calculate_program_invoice_price(user_id=current_user.id)
        # (selected modes, unselected active modes)
        return render_template('user_program.html',
                               selected_modes=selected_unselected_modes[0],
                               unselected_modes=selected_unselected_modes[1],
                               program_price=price_with_discount,
                               user_id=current_user.id)
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('user.user_profile'))


@user.route('/program/add-mode/<int:user_id>/<int:mode_id>', methods=['GET'])
@login_required
def user_program_add_mode(user_id: int, mode_id: int):
    try:
        post_mode_in_program(mode_id=mode_id, user_id=user_id)
        return redirect(url_for('user.user_program'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('user.user_program'))


@user.route('/program/remove-mode/<int:user_id>/<int:mode_id>', methods=['GET'])
@login_required
def user_program_remove_mode(mode_id: int, user_id: int):
    try:
        delete_mode_from_program(mode_id=mode_id, user_id=user_id)
        return redirect(url_for('user.user_program'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('user.user_program'))


@user.route('/program/create-invoice', methods=['GET'])
@login_required
def user_create_invoice():
    try:
        discounted_price = calculate_program_invoice_price(user_id=current_user.id)
        print('discounted price: ', discounted_price)
        new_invoice = Invoice(price=discounted_price, user_id=current_user.id)
        post_create_new_invoice(new_invoice)
        return redirect(url_for('user.user_program'))
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('user.user_program'))
