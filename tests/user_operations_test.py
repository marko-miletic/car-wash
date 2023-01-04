from src.database.session import SessionLocal
from src.crud import user_operations
from src.models import User


session = SessionLocal()


def test_get_all_users():
    users = user_operations.get_all_users()

    assert len(users) != 0 and \
           users[0].get('id') is not None


def test_get_user_by_status():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    admin_users = user_operations.get_user_by_status(status='admin')
    user_users = user_operations.get_user_by_status(status='user')
    all_users = user_operations.get_all_users()

    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()
    
    assert len(admin_users) != 0 \
           and len(user_users) != 0 \
           and admin_users[0].get('id') is not None \
           and user_users[0].get('id') is not None \
           and len(admin_users) + len(user_users) == len(all_users)
