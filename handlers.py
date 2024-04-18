import requests
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from utils import calculate_offer_1
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

exchange_rate_url = 'https://api.exchangerate-api.com/v4/latest/RUB'


def get_currency_button():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Текущий курс валют', callback_data='get_currency')]])
    return keyboard


@router.message(Command('start'))
async def start(message: Message):
    try:
        await message.answer(text='Привет! Чтобы узнать текущий курс валют, нажмите кнопку ниже', reply_markup=get_currency_button())

    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}.')


@router.message(lambda message: message.text == 'Рассчитать заявку')
async def calculate_offer(message: Message):
    await message.answer(text='Введите сумму авто (в йенах)')


# @router.message()
# async def calculate_offer(message: Message):
#     if message.text.isdigit():
#         car_price = int(message.text)
#         amount = calculate_offer_1(car_price)
#         await message.answer(text=
#                              f'Сумма расходов в Японии:\n <b>{amount}</b> рублей, из них:\n'
#                              f'Цена машины: <b>{car_price}</b>\n'
#                              f'Фрахт: <b>400$</b>\n',
#                              parse_mode='html')


@router.callback_query()
async def current_currency(callback_query: types.CallbackQuery):
    try:
        response = requests.get(exchange_rate_url)
        data = response.json()

        timestamp = data['time_last_updated']
        date_time = datetime.fromtimestamp(timestamp).strftime('%H:%M час. %d.%m.%Y')

        usd_rate = data['rates']['USD']
        eur_rate = data['rates']['EUR']
        jpy_rate = data['rates']['JPY']
        cny_rate = data['rates']['CNY']

        exchange_rate_message = f'Текущий курс валют относительно рубля на <b>{date_time}</b>:\n\n' \
                                f'Евро: <b>{round((1 / eur_rate), 2)}</b> руб.\n' \
                                f'Доллар США: <b>{round((1 / usd_rate), 2)}</b> руб.\n'\
                                f'Японская Иена: <b>{round((1 / jpy_rate), 2)}</b> руб.\n' \
                                f'Китайский Юань: <b>{round((1 / cny_rate), 2)}</b> руб.\n'

        await callback_query.answer()
        await callback_query.message.answer(exchange_rate_message, parse_mode='html')

    except Exception as e:
        await callback_query.answer(f'Произошла ошибка при получении текущего курса валют: {e}.')
