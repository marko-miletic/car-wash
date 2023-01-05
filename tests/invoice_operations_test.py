from src.crud import invoice_operations
from src.database.session import SessionLocal
from src.models import Invoice, User


session = SessionLocal()


def test_post_create_new_invoice():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_invoice = Invoice(price=-1, user_id=test_user.id)
    test_invoice.id = -1

    invoice_operations.post_create_new_invoice(test_invoice)

    invoice = session.query(Invoice).filter(Invoice.id == test_invoice.id).first()

    session.query(Invoice).filter(Invoice.id == test_invoice.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert invoice is not None and invoice.id == test_invoice.id


def test_get_count_user_invoices():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_invoice = Invoice(price=-1, user_id=test_user.id)
    test_invoice.id = -1

    session.add(test_invoice)
    session.commit()

    invoice_count = invoice_operations.get_count_user_invoices(user_id=test_user.id)

    session.query(Invoice).filter(Invoice.id == test_invoice.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert invoice_count == 1


def test_get_pending_invoices():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_invoice = Invoice(price=-1, user_id=test_user.id)
    test_invoice.id = -1

    session.add(test_invoice)
    session.commit()

    pending_invoices = invoice_operations.get_pending_invoices()

    session.query(Invoice).filter(Invoice.id == test_invoice.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert pending_invoices and [True for invoice in pending_invoices if invoice.get('id') == -1]


def test_update_invoice_completed_status():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_invoice = Invoice(price=-1, user_id=test_user.id)
    test_invoice.id = -1

    session.add(test_invoice)
    session.commit()

    invoice_operations.update_invoice_completed_status(invoice_id=-1)

    updated_invoice = session.query(Invoice).filter(Invoice.id == test_invoice.id).first()

    session.query(Invoice).filter(Invoice.id == test_invoice.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert updated_invoice.completed is True
