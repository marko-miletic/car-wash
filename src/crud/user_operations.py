from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.core.roles import role_names
from src.database.session import SessionLocal
from src.models import User


session = SessionLocal()


def get_all_users() -> list:
    users_template = ['id', 'name', 'email', 'car_registration', 'role']
    try:
        users = session.query(User.id, User.name, User.email, User.car_registration, User.role).all()
        print([dict(zip(users_template, tuple(row))) for row in users])
        return [dict(zip(users_template, tuple(row))) for row in users]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def get_user_by_status(status: str = 'admin') -> list:
    users_template = ['id', 'name', 'email', 'car_registration']
    try:
        users = session.query(User.id, User.name, User.email, User.car_registration)\
            .filter(User.role == role_names(status))\
            .all()
        return [dict(zip(users_template, tuple(row))) for row in users]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err
