from src.database import session
from src.database import preload_db_util


session = session.SessionLocal()


def fill_db_data() -> None:
    preload_db_util.add_default_admin_user()
    preload_db_util.add_default_discount_data()
