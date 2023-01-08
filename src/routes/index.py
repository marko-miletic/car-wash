from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from src.logs import logger
from src.crud.discount_operations import get_current_discount_data
from src.crud.mode_operations import get_modes_by_active_status
from src.path_structure import TEMPLATES_DIRECTORY_PATH


index = Blueprint('index', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@index.route('/')
def main():
    try:
        discount_data = get_current_discount_data()
        active_washing_modes = get_modes_by_active_status(active_status=True)
        return render_template('index.html',
                               discount_data=discount_data,
                               active_modes=active_washing_modes)
    except Exception as err:
        logger.logging.error(err)
        return render_template('index.html')
