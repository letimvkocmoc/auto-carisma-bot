import os

import requests
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from database.utils import SQL
from utils import calculate_offer
from datetime import datetime
from keyboards.inline import set_admin_inline_keyboard
from database import utils

router = Router()
sql = SQL()
admin_ids = os.getenv('ADMIN_IDS')
exchange_rate_url = 'https://api.exchangerate-api.com/v4/latest/RUB'
admin_keyboard = set_admin_inline_keyboard()


@router.message(Command('start'))
async def start(message: Message):
    try:
        await message.answer(text='Привет! Выбери кнопку из меню ниже',
                             reply_markup=admin_keyboard)
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}.')


#@router.message(lambda message: message.text == 'Рассчитать заявку')
#async def calculate_offer(message: Message):
    #await message.answer(text='Введите сумму авто (в йенах)')


@router.callback_query(lambda callback_query: callback_query.data == 'get_currency')
async def get_currency(callback_query: types.CallbackQuery):
    if str(callback_query.from_user.id) in admin_ids:
        try:
            response = requests.get(exchange_rate_url)
            data = response.json()
            timestamp = data['time_last_updated']
            date_time = datetime.fromtimestamp(timestamp).strftime('%H:%M час. %d.%m.%Y')
            date_time_db = datetime.fromtimestamp(timestamp)

            eur_rate = data['rates']['EUR']
            usd_rate = data['rates']['USD']
            jpy_rate = data['rates']['JPY']
            cny_rate = data['rates']['CNY']

            sql.update(1, rate=round((1 / eur_rate), 2), updated=date_time_db, last_request=datetime.now())
            sql.update(2, rate=round((1 / usd_rate), 2), updated=date_time_db, last_request=datetime.now())
            sql.update(3, rate=round((1 / jpy_rate), 2), updated=date_time_db, last_request=datetime.now())
            sql.update(4, rate=round((1 / cny_rate), 2), updated=date_time_db, last_request=datetime.now())

            exchange_rate_message = f'Текущий курс валют на <b>{date_time}</b>:\n\n' \
                                    f'🇪🇺 Евро: <b>{round((1 / eur_rate), 2)}</b> ₽.\n' \
                                    f'🇺🇸 Доллар США: <b>{round((1 / usd_rate), 2)}</b> ₽.\n' \
                                    f'🇯🇵 Японская Иена: <b>{round((1 / jpy_rate), 2)}</b> ₽.\n' \
                                    f'🇨🇳 Китайский Юань: <b>{round((1 / cny_rate), 2)}</b> ₽.\n'

            await callback_query.answer()
            await callback_query.message.answer(exchange_rate_message, parse_mode='html')

        except Exception as e:
            await callback_query.answer(f'Произошла ошибка при получении текущего курса валют: {e}.')
    else:
        await callback_query.message.edit_text('Вы не админ.')


@router.callback_query(lambda callback_query: callback_query.data == 'get_japan_consumptions')
async def get_japan_consumptions(callback_query: types.CallbackQuery):
    if str(callback_query.from_user.id) in admin_ids:
        try:
            await callback_query.message.answer(text='Введите стоимость авто в йенах')

        except Exception as e:
            await callback_query.answer(f'Произошла ошибка: {e}.')
    else:
        await callback_query.message.edit_text('Вы не админ.')


@router.message(lambda message: message.text.isdigit() and int(message.text) > 0)
async def get_japan_consumptions(message: types.Message):
    if str(message.from_user.id) in admin_ids:
        try:
            car_price = int(message.text)
            japan_consumptions = calculate_offer(car_price)
            await message.answer(text=f'Расходы по Японии составят: <b>{japan_consumptions}</b> рублей.', parse_mode='html')
        except Exception as e:
            await message.answer(f'Произошла ошибка: {e}.')
    else:
        await message.edit_text('Вы не админ.')
