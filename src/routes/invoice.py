from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from src.logs import logger
from src.core.roles import role_names
from src.crud.invoice_operations import get_invoice_related_modes, get_invoice_user_id
from src.path_structure import TEMPLATES_DIRECTORY_PATH


invoice = Blueprint('invoice', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@login_required
@invoice.route('/<int:invoice_id>')
def invoice_get_modes(invoice_id: int):
    try:
        # gets user id and checks for access permission to requested invoice
        # 1. user has access only to his own invoices
        # 2. admin has access to all invoices
        invoice_user_id = get_invoice_user_id(invoice_id=invoice_id)
        if invoice_user_id != current_user.id and current_user.role != role_names(role='admin'):
            return redirect(url_for('index.main'))
        invoice_modes = get_invoice_related_modes(invoice_id=invoice_id)
        return render_template('invoice_modes.html',
                               invoice_modes=invoice_modes)
    except Exception as err:
        logger.logging.error(err)
        return redirect(url_for('index.main'))
