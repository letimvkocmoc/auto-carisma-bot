from aiogram import Bot

from core.utils import update_currency_rate
from database.utils import SQL

sql = SQL()


async def get_currency_rate(bot: Bot):
    try:
        update_currency_rate()
        currencies = sql.get_currencies()
        admin_ids = [367150414]
        for admin in admin_ids:
            await bot.send_message(chat_id=admin, text='Курс валют успешно обновлен ✅\n\n'
                                                       f'📈 Текущий курс валют на <b>{currencies["updated"]}</b>:\n\n' \
                                                       f'🇪🇺 Евро: <b>{currencies["currency"]["EUR"]}</b> ₽\n' \
                                                       f'🇺🇸 Доллар США: <b>{currencies["currency"]["USD"]}</b> ₽\n' \
                                                       f'🇯🇵 Японская Иена: <b>{currencies["currency"]["JPY"]}</b> ₽\n' \
                                                       f'🇨🇳 Китайский Юань: <b>{currencies["currency"]["CNY"]}</b> ₽\n',
                                   parse_mode='HTML')
    except Exception as e:
        for admin in admin_ids:
            await bot.send_message(chat_id=admin, text=f'Ошибка при обновлении курса валют: {e}')