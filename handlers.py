from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils import calculate_offer_1

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')


@router.message(lambda message: message.text == 'Рассчитать заявку')
async def calculate_offer(message: Message):
    await message.answer(text='Введите сумму авто (в йенах)')


@router.message()
async def calculate_offer(message: Message):
    if message.text.isdigit():
        car_price = int(message.text)
        amount = calculate_offer_1(car_price)
        await message.answer(text=
                             f'Сумма расходов в Японии:\n <b>{amount}</b> рублей, из них:\n'
                             f'Цена машины: <b>{car_price}</b>\n'
                             f'Фрахт: <b>400$</b>\n',
                             parse_mode='html')

