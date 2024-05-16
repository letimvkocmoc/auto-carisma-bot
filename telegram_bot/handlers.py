from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from database.utils import SQL
from core.utils import calculate_offer
from keyboards.inline import set_admin_inline_keyboard, create_link

router = Router()
admin_ids = [588120104, 367150414]
admin_keyboard = set_admin_inline_keyboard()
sql = SQL()


@router.message(Command('start'))
async def start(message: Message):
    try:
        await message.answer(text='Привет! Выбери кнопку из меню ниже',
                             reply_markup=admin_keyboard)
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}.')


# @router.callback_query(lambda callback_query: callback_query.data == 'get_currency')
# async def get_currency(callback_query: types.CallbackQuery):
#     if callback_query.from_user.id in admin_ids:
#         try:
#             exchange_rate_message = f'📈 Текущий курс валют на <b>{currencies["updated"]}</b>:\n\n' \
#                                     f'🇪🇺 Евро: <b>{currencies["currency"]["EUR"]}</b> ₽\n' \
#                                     f'🇺🇸 Доллар США: <b>{currencies["currency"]["USD"]}</b> ₽\n' \
#                                     f'🇯🇵 Японская Иена: <b>{currencies["currency"]["JPY"]}</b> ₽\n' \
#                                     f'🇨🇳 Китайский Юань: <b>{currencies["currency"]["CNY"]}</b> ₽\n'
#
#             await callback_query.answer()
#             await callback_query.message.edit_text(exchange_rate_message, parse_mode='html')
#
#         except Exception as e:
#             await callback_query.answer(f'Произошла ошибка при получении текущего курса валют: {e}.')
#     else:
#         await callback_query.message.edit_text('Вы не админ.')


@router.callback_query(lambda callback_query: callback_query.data == 'get_japan_consumptions')
async def get_japan_consumptions(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in admin_ids:
        try:
            await callback_query.message.answer(text='Введите стоимость авто в йенах')

        except Exception as e:
            await callback_query.answer(f'Произошла ошибка: {e}.')
    else:
        await callback_query.message.edit_text('Вы не админ.')


@router.message(lambda message: message.text.isdigit() and int(message.text) > 0)
async def get_japan_consumptions(message: types.Message):
    if message.from_user.id in admin_ids:
        try:
            car_price = int(message.text)
            japan_consumptions = calculate_offer(car_price)
            await message.answer(text=f'Расходы по Японии составят: <b>{japan_consumptions}</b> рублей.', parse_mode='html')
        except Exception as e:
            await message.answer(f'Произошла ошибка: {e}.')
    else:
        await message.edit_text('Вы не админ.')


@router.callback_query(lambda callback_query: callback_query.data == 'orders')
async def get_orders(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in admin_ids:
        try:
            orders = sql.get_orders()
            for order in orders:
                keyboard = create_link(1, link=order[10], text='Открыть аукцион', id=order[0])
                await callback_query.message.answer_photo(photo=f"{order[9]}",
                                                          caption=f"🔎 <b>Заявка № {order[0]}</b>\n"
                                                                  f"🔹 <b>Имя:</b> {order[2]}\n"
                                                                  f"🔹 <b>Фамилия:</b> {order[3]}\n"
                                                                  f"🔹 <b>Телеграм ID:</b> <a href='tg://user?id={order[1]}'>{order[1]}</a>\n"
                                                                  f"☎️ <b>Номер телефона:</b> <a href='tel:{order[4]}'>{order[4]}</a>\n"
                                                                  f"🚗 <b>Марка авто:</b> {order[5]}\n"
                                                                  f"⭐️ <b>Оценка:</b> {order[6]}\n"
                                                                  f"💵 <b>Стоимость:</b> {order[7]} ₽\n"
                                                                  f"📍 <b>Статус:</b> {order[8]}\n"
                                                                  f"💰 <b>Оплачен:</b> {'✅' if order[11] else '❌'}\n",
                                                          parse_mode='html', reply_markup=keyboard)
        except Exception as e:
            await callback_query.message.answer(text=f'Какая то хуйня: {e}')
    else:
        await callback_query.message.answer(text='Вы не админ.')
