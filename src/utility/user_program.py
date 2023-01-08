from src.logs import logger
from src.crud.mode_operations import get_user_selected_modes, get_modes_by_active_status


def get_user_selected_and_available_modes(user_id: int) -> tuple:
    """
    function:
        Creates two lists of washing modes.
        1. First list contains modes that are already selected in user's program.
        2. Second list contains modes that are both currently available (active) and
           not contained in user's current program.

    parameters:
        user_id: int - parameter used for getting washing modes in current user program

    return:
        tuple[list, list]: contains separated user available modes
    """
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
