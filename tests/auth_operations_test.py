from src.database.session import SessionLocal
from src.crud import auth_operations
from src.models import User


session = SessionLocal()


def test_blank_get_user_by_id():
    blank_user_id = -1

    user = auth_operations.get_user_by_id(blank_user_id)

    assert user is None


def test_blank_get_user_by_email():
    user = auth_operations.get_user_by_email('')

    assert user is None


def test_get_user_by_id():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    user = auth_operations.get_user_by_id(test_user.id)

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert user is not None


def test_get_user_by_email():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    user = auth_operations.get_user_by_email(test_user.email)

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert user is not None


def test_post_create_new_user():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    auth_operations.post_create_new_user(test_user)

    user = session.query(User).filter(User.id == test_user.id).first()

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert user is not None
