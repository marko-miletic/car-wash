import os


SRC_DIRECTORY_PATH = os.path.split(os.path.abspath(__file__))[0]

CORE_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'core')
DATABASE_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'database')
MODELS_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'models')
ROUTES_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'routes')
TEMPLATES_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'templates')
SERVICES_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'crud')
LOGS_DIRECTORY_PATH = os.path.join(SRC_DIRECTORY_PATH, 'logs')
