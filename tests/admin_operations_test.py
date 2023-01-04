from src.database.session import SessionLocal
from src.models import User
from src.crud import admin_operations


session = SessionLocal()


def test_update_change_user_status():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    new_user_role = 1

    admin_operations.update_change_user_status(new_role='admin', user_id=test_user.id)

    test_user_role = session.query(User.role).filter(User.id == test_user.id).scalar()
    print(test_user_role)

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert test_user_role == new_user_role


def test_update_change_user_status_wrong_input():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    previous_user_role = test_user.role  # role defaults to 0

    admin_operations.update_change_user_status(new_role='wrong-user-role', user_id=test_user.id)

    test_user_role = session.query(User.role).filter(User.id == test_user.id).scalar()

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert test_user_role == previous_user_role
