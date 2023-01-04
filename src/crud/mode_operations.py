from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Mode, Program


session = SessionLocal()


def post_create_new_mode(new_mode_object: Mode) -> None:
    try:
        session.add(new_mode_object)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def get_modes_by_active_status(active_status: bool = True) -> list:
    modes_template = ['id', 'description', 'price', 'active']
    try:
        modes = session.query(Mode.id, Mode.description, Mode.price, Mode.active)\
            .filter(Mode.active == active_status)\
            .all()
        return [dict(zip(modes_template, tuple(row))) for row in modes]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def update_change_mode_active_status(new_status: bool, mode_id: int) -> None:
    try:
        session.query(Mode)\
            .filter(Mode.id == mode_id)\
            .update({Mode.active: new_status})
        session.commit()
        if new_status is False:
            session.query(Program)\
                .filter(Program.mode_id == mode_id)\
                .delete()
            session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def get_user_selected_modes(user_id: int) -> list:
    modes_template = ['id', 'description', 'price']
    try:
        modes = session.query(Mode.id, Mode.description, Mode.price)\
            .join(Program)\
            .filter(Program.user_id == user_id)\
            .all()
        return [dict(zip(modes_template, tuple(row))) for row in modes]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err
