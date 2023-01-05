from src.logs import logger
from src.crud.mode_operations import get_user_selected_modes, get_modes_by_active_status


def get_user_selected_and_available_modes(user_id: int) -> tuple:  # (selected modes, unselected active modes)
    try:
        selected_modes = get_user_selected_modes(user_id=user_id)
        all_active_modes = get_modes_by_active_status(active_status=True)

        selected_modes_id_set = {mode.get('id', -1) for mode in selected_modes}
        user_unselected_active_modes = [mode for mode in all_active_modes
                                        if mode.get('id', None) not in selected_modes_id_set]
        return selected_modes, user_unselected_active_modes
    except Exception as err:
        logger.logging.error(err)
        raise ValueError(err)
