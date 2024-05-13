from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def set_admin_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Рассчитать стоимость расходов по Японии',
                                  callback_data='get_japan_consumptions')],
            [InlineKeyboardButton(text='Текущий курс валют', callback_data='get_currency')],
            [InlineKeyboardButton(text='Список заявок', callback_data='orders')]
        ])
    return keyboard


def create_link(width: int, link, text: str | None = None, id: str | None = None):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text=text, web_app=WebAppInfo(url=link)),
        InlineKeyboardButton(text='Открыть на сайте', url='http://127.0.0.1:5000/edit/{id}'.format(id=id)),
        width=width)
    return kb_builder.as_markup()
