from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.models import Discount


session = SessionLocal()


def get_current_discount_data() -> Discount:
    try:
        discount = session.query(Discount)\
            .order_by(desc(Discount.valid_since))\
            .first()
        return discount
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def post_create_new_discount(new_discount_object: Discount) -> None:
    try:
        session.add(new_discount_object)
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
