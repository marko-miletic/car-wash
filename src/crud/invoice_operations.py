from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError

from src.logs import logger
from src.database.session import SessionLocal
from src.crud.mode_operations import get_user_selected_modes
from src.models import Invoice, User, InvoiceModes, Mode


session = SessionLocal()


def get_invoice_user_id(invoice_id: int) -> int:
    try:
        user_id = session.query(Invoice.user_id).filter(Invoice.id == invoice_id).scalar()
        return user_id
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def post_invoice_modes(user_id: int, invoice_id: int) -> None:
    try:
        current_program_modes = get_user_selected_modes(user_id=user_id)
        list_mode_id = [mode.get('id', None) for mode in current_program_modes]
        for mode_id in list_mode_id:
            new_invoice_mode = InvoiceModes(invoice_id=invoice_id, mode_id=mode_id)
            session.add(new_invoice_mode)
            session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def post_create_new_invoice(user_id: int, new_invoice_object: Invoice) -> None:
    try:
        session.add(new_invoice_object)
        session.commit()
        post_invoice_modes(user_id=user_id, invoice_id=new_invoice_object.id)
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err


def get_invoice_related_modes(invoice_id: int) -> list:
    invoices_modes_template = ['id', 'invoice_id', 'mode_description', 'price']
    try:
        invoice_modes = session.query(InvoiceModes.id, Invoice.id, Mode.description, Mode.price)\
            .join(Invoice)\
            .join(Mode)\
            .filter(InvoiceModes.invoice_id == invoice_id)\
            .all()
        return [dict(zip(invoices_modes_template, tuple(row))) for row in invoice_modes]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def get_user_invoices(user_id: int, number: int = None) -> list:
    invoices_template = ['id', 'user', 'price', 'completed']
    try:
        invoices = session.query(Invoice.id, User.name, Invoice.price, Invoice.completed)\
            .join(User)\
            .filter(Invoice.user_id == user_id)
        if number is None:
            invoices = invoices.order_by(desc(Invoice.time_stamp)).all()
        else:
            invoices = invoices.limit(number).order_by(desc(Invoice.time_stamp)).all()
        return [dict(zip(invoices_template, tuple(row))) for row in invoices]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def get_split_user_invoices(user_id: int, split_number: int = None) -> tuple:
    try:
        invoices = get_user_invoices(user_id=user_id)
        if len(invoices) <= split_number:
            return invoices, list()
        return invoices[:split_number], invoices[split_number:]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def get_count_user_invoices(user_id: int) -> int:
    try:
        user_invoice_count = session.query(func.count(Invoice.id))\
            .filter(Invoice.user_id == user_id) \
            .scalar()
        return user_invoice_count
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def get_pending_invoices() -> list:
    invoices_template = ['id', 'user', 'price', 'car_registration']
    try:
        invoices = session.query(Invoice.id, User.name, Invoice.price, User.car_registration) \
            .join(User) \
            .filter(Invoice.completed == False) \
            .all()
        return [dict(zip(invoices_template, tuple(row))) for row in invoices]
    except SQLAlchemyError as err:
        logger.logging.error(err)
        raise err


def update_invoice_completed_status(invoice_id: int, new_status: bool = True) -> None:
    try:
        session.query(Invoice)\
            .filter(Invoice.id == invoice_id)\
            .update({Invoice.completed: new_status})
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.logging.error(err)
        raise err
