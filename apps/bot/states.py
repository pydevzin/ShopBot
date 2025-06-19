from aiogram.fsm.state import StatesGroup, State

class RegistrationStateGroup(StatesGroup):
    language = State()
    fullname = State()
    phone = State()
    back = State()


class CategoryStateGroup(StatesGroup):
    main_category = State()
    sub_category = State()
    product_list = State()

