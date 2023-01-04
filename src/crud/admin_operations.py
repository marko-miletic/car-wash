from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.core.roles import role_names
from src.database.session import SessionLocal
from src.models import User


session = SessionLocal()


def update_change_user_status(new_role: str, user_id: int) -> None:
    try:
        session.query(User).filter(User.id == user_id).update({User.role: role_names(new_role)})
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
