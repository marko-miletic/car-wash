from src.database.session import SessionLocal
from src.crud import discount_operations
from src.models import Discount


session = SessionLocal()


def test_get_current_discount_data():
    test_discount = Discount(base_discount=-1,
                             additional_discount=-1,
                             additional_discount_description='-')
    test_discount.id = -1

    session.add(test_discount)
    session.commit()

    discount = discount_operations.get_current_discount_data()

    session.query(Discount).filter(Discount.id == test_discount.id).delete()
    session.commit()

    assert discount is not None and discount.id == -1


def test_post_create_new_discount():
    test_discount = Discount(base_discount=-1,
                             additional_discount=-1,
                             additional_discount_description='-')
    test_discount.id = -1

    discount_operations.post_create_new_discount(new_discount_object=test_discount)

    discount = session.query(Discount.id).filter(Discount.id == test_discount.id).first()

    session.query(Discount).filter(Discount.id == test_discount.id).delete()
    session.commit()

    assert discount is not None and discount.id == -1
