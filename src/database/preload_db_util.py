from werkzeug.security import generate_password_hash

from src.models import User, Discount
from src.database import session
from src.core.config import admin_default_account


session = session.SessionLocal()


def add_default_admin_user() -> None:
    # checks if there is already required data in db
    test_sample_query = session.query(User).filter(User.name == admin_default_account.USER).scalar()
    if test_sample_query:
        return None

    default_admin_user = User(name=admin_default_account.USER, email=admin_default_account.MAIL,
                              password=generate_password_hash(admin_default_account.PASSWORD, method='sha256'),
                              car_registration='x-x-x', role=1)

    session.add(default_admin_user)
    session.commit()


def add_default_discount_data() -> None:
    # checks if there is already required data in db
    test_sample_query = session.query(Discount).first()
    if test_sample_query:
        return None

    default_discount_data = Discount(base_discount=10, additional_discount=0, additional_discount_description='-')

    session.add(default_discount_data)
    session.commit()
