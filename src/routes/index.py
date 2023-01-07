from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from src.logs import logger
from src.path_structure import TEMPLATES_DIRECTORY_PATH


index = Blueprint('index', __name__, template_folder=TEMPLATES_DIRECTORY_PATH)


@index.route('/')
def main():
    return render_template('index.html')
