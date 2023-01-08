from src.logs import logger
from src.crud.mode_operations import get_user_selected_modes
from src.crud.discount_operations import get_current_discount_data
from src.crud.invoice_operations import get_count_user_invoices


def calculate_program_invoice_price(user_id: int) -> float:
    """
    function:
        Calculates price for user's washing program based on current discount values.
        Steps:
        1. Calculates total program cost.
        2. Applies additional discount percentage if there is one currently.
        3. Applies base discount percentage on price calculated in step 2.
           ( this discount is applied only if number of user's invoices is divisible by 10)
    parameters:
        user_id: int - parameter used for getting washing modes in current user program

    return:
        float: price after all discount options are applied
    """
    try:
        current_discount_data = get_current_discount_data()
        current_user_program = get_user_selected_modes(user_id=user_id)
        user_invoices_count = get_count_user_invoices(user_id=user_id)

        # step 1
        total_modes_price = 0
        for mode in current_user_program:
            total_modes_price += mode.get('price', 0)

        # step 2
        discounted_price = total_modes_price -\
                           ((current_discount_data.additional_discount / 100) * total_modes_price)

        # step 3
        if user_invoices_count % 10 == 0 and user_invoices_count != 0:
            discounted_price = discounted_price -\
                               ((current_discount_data.base_discount / 100) * discounted_price)
        return round(discounted_price, 2)
    except Exception as err:
        logger.logging.error(err)
        raise ValueError(err)
