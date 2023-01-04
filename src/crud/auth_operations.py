from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import User


session = SessionLocal()


def get_user_by_id(user_id: int) -> tuple:
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def get_user_by_email(email: str) -> User:
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def post_create_new_user(new_user_object: User) -> None:
    try:
        session.add(new_user_object)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
