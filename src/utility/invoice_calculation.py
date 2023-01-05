from src.logs import logger
from src.crud.mode_operations import get_user_selected_modes
from src.crud.discount_operations import get_current_discount_data
from src.crud.invoice_operations import get_count_user_invoices


def calculate_program_invoice_price(user_id: int) -> float:  # (selected modes, unselected active modes)
    try:
        current_discount_data = get_current_discount_data()
        current_user_program = get_user_selected_modes(user_id=user_id)
        user_invoices_count = get_count_user_invoices(user_id=user_id)

        total_modes_price = 0
        for mode in current_user_program:
            total_modes_price += mode.get('price', 0)

        print('modes price: ', total_modes_price)

        discounted_price = total_modes_price -\
                           ((current_discount_data.additional_discount / 100) * total_modes_price)

        print('discount 1: ', discounted_price)

        if user_invoices_count % 10 == 0 and user_invoices_count != 0:
            discounted_price = discounted_price -\
                               ((current_discount_data.base_discount / 100) * discounted_price)
        return discounted_price
    except Exception as err:
        logger.logging.error(err)
        raise ValueError(err)
