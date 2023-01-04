from werkzeug.security import generate_password_hash

from src import models
from src.database import session
from src.core.config import admin_default_account


session = session.SessionLocal()


def add_default_admin_user() -> None:
    test_sample_query = session.query(models.User).filter(models.User.name == admin_default_account.USER).scalar()
    if test_sample_query:
        return None

    default_admin_user = models.User(
        name=admin_default_account.USER,
        email=admin_default_account.MAIL,
        password=generate_password_hash(admin_default_account.PASSWORD, method='sha256'),
        car_registration='x-x-x',
        role=1
    )

    session.add(default_admin_user)
    session.commit()
