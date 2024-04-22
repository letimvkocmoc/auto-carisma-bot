from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def set_admin_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Текущий курс валют', callback_data='get_currency')],
            [InlineKeyboardButton(text='Рассчитать стоимость расходов по Японии', callback_data='get_japan_consumptions')]
        ])
    return keyboard
