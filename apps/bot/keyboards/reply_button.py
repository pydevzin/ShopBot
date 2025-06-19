from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_phone_number():
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='send phone', request_contact=True)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


