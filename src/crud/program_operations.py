from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Program


session = SessionLocal()


def delete_mode_from_program(mode_id: int, user_id: int) -> None:
    try:
        session.query(Program)\
            .filter(and_(Program.mode_id == mode_id, Program.user_id == user_id))\
            .delete()
        session.commit()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def post_mode_in_program(mode_id: int, user_id: int) -> None:
    try:
        new_program = Program(mode_id=mode_id, user_id=user_id)
        session.add(new_program)
        session.commit()
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err
