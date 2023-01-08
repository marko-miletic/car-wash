from flask import Flask

from src import routes
from src.core.config import auth_app_settings
from src.core.authentication import login_manager
from src.crud.auth_operations import get_user_by_id
from src.database.preload_db_data import fill_db_data


def build_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = auth_app_settings.AUTH_SECRET_KEY

    app.register_blueprint(routes.index, url_prefix='/')
    app.register_blueprint(routes.auth, url_prefix='/auth')
    app.register_blueprint(routes.admin, url_prefix='/admin')
    app.register_blueprint(routes.mode, url_prefix='/mode')
    app.register_blueprint(routes.user, url_prefix='/user')
    app.register_blueprint(routes.invoice, url_prefix='/invoice')
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    from src.core.cache import cache
    cache.init_app(app=app)

    fill_db_data()

    return app
