from src.crud import program_operations
from src.database.session import SessionLocal
from src.models import Program, User, Mode


session = SessionLocal()


def test_post_mode_in_program():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_mode = Mode(description='test', price=-1)
    test_mode.id = -1

    session.add(test_mode)
    session.commit()

    program_operations.post_mode_in_program(mode_id=test_mode.id, user_id=test_user.id)

    test_program = session.query(Program).filter(Program.mode_id == test_mode.id).first()

    session.query(Program).filter(Program.mode_id == test_mode.id).delete()
    session.query(Mode).filter(Mode.id == test_mode.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert test_program is not None and test_program.user_id == test_user.id


def test_delete_mode_from_program():
    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_mode = Mode(description='test', price=-1)
    test_mode.id = -1

    session.add(test_mode)
    session.commit()

    test_program = Program(mode_id=test_mode.id, user_id=test_user.id)

    session.add(test_program)
    session.commit()

    program_operations.delete_mode_from_program(mode_id=test_mode.id, user_id=test_user.id)

    deleted_mode = session.query(Program).filter(Program.mode_id == test_mode.id).first()

    session.query(Program).filter(Program.mode_id == test_mode.id).delete()
    session.query(Mode).filter(Mode.id == test_mode.id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert deleted_mode is None
