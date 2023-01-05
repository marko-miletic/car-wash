from src.database.session import SessionLocal
from src.crud import mode_operations
from src.models import Mode, Program, User


session = SessionLocal()


def test_post_create_new_mode():
    test_mode = Mode(description='-', price=-1)
    test_mode.id = -1

    mode_operations.post_create_new_mode(test_mode)

    mode = session.query(Mode).filter(Mode.id == test_mode.id).first()

    session.query(Mode).filter(Mode.id == test_mode.id).delete()
    session.commit()

    assert mode is not None and mode.id == test_mode.id


def test_get_modes_by_active_status():
    test_mode_active = Mode(description='-', price=-1)
    test_mode_active.active = True
    test_mode_active.id = -1

    test_mode_inactive = Mode(description='--', price=-1)
    test_mode_inactive.active = False
    test_mode_inactive.id = -2

    session.add(test_mode_active)
    session.add(test_mode_inactive)
    session.commit()

    active_modes = mode_operations.get_modes_by_active_status(active_status=True)
    inactive_modes = mode_operations.get_modes_by_active_status(active_status=False)

    session.query(Mode).filter(Mode.id == test_mode_active.id).delete()
    session.query(Mode).filter(Mode.id == test_mode_inactive.id).delete()
    session.commit()

    assert len(active_modes) != 0 \
           and len(inactive_modes) != 0 \
           and active_modes[0].get('active') is True \
           and inactive_modes[0].get('active') is False


def test_update_change_mode_active_status():
    test_mode = Mode(description='-', price=-1)
    test_mode.active = True
    test_mode.id = -1

    session.add(test_mode)
    session.commit()

    test_user = User(name='test', email='test', password='test', car_registration='test')
    test_user.id = -1

    session.add(test_user)
    session.commit()

    test_program = Program(mode_id=test_mode.id, user_id=test_user.id)
    test_program.id = -1

    session.add(test_program)
    session.commit()

    mode_operations.update_change_mode_active_status(new_status=False, mode_id=test_mode.id)
    inactive_status = session.query(Mode.active).filter(Mode.id == test_mode.id).scalar()
    programs_with_inactive_mode = session.query(Program).filter(Program.mode_id == test_mode.id).one_or_none()

    mode_operations.update_change_mode_active_status(new_status=True, mode_id=test_mode.id)
    active_status = session.query(Mode.active).filter(Mode.id == test_mode.id).scalar()

    test_program_id = -1

    session.query(Mode).filter(Mode.id == test_mode.id).delete()
    session.query(Program).filter(Program.id == test_program_id).delete()
    session.query(User).filter(User.id == test_user.id).delete()
    session.commit()

    assert inactive_status is False and active_status is True and programs_with_inactive_mode is None
