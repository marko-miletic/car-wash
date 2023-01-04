import os
import logging

from src.path_structure import LOGS_DIRECTORY_PATH


LOGS_PATH = os.path.join(LOGS_DIRECTORY_PATH, 'log_data')


logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(LOGS_PATH, 'log_data.log'),
                    format="%(asctime)s :: %(levelname)s :: %(message)s")
