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


@router.callback_query(lambda callback_query: callback_query.data == 'get_currency')
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

        exchange_rate_message = f'Текущий курс валют на <b>{date_time}</b>:\n\n' \
                                f'Евро: <b>{round((1 / eur_rate), 2)}</b> ₽\n' \
                                f'Доллар США: <b>{round((1 / usd_rate), 2)}</b> ₽\n'\
                                f'Японская Иена: <b>{round((1 / jpy_rate), 2)}</b> ₽\n' \
                                f'Китайский Юань: <b>{round((1 / cny_rate), 2)}</b> ₽\n'

        await callback_query.answer()
        await callback_query.message.answer(exchange_rate_message, parse_mode='html')

    except Exception as e:
        await callback_query.answer(f'Произошла ошибка при получении текущего курса валют: {e}.')
