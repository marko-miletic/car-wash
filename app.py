from src.build.create_app import build_app
from src.core.config import app_server_settings


if __name__ == "__main__":

    build_app().run(
        host=app_server_settings.HOST,
        port=app_server_settings.PORT,
        debug=app_server_settings.DEBUG
    )
