import os

from aiogram import Bot

from core.utils import update_currency_rate


async def get_currency_rate(bot: Bot):
    try:
        currencies = update_currency_rate()
        admin_ids = [367150414]
        for admin in admin_ids:
            await bot.send_message(chat_id=admin, text='Курс валют успешно обновлен ✅\n\n'
                                               f'Текущий курс валют на <b>{currencies['updated']}</b>:\n\n' \
                                               f'🇪🇺 Евро: <b>{currencies['currencies']['EUR']}</b> ₽\n' \
                                               f'🇺🇸 Доллар США: <b>{currencies['currencies']['USD']}</b> ₽\n' \
                                               f'🇯🇵 Японская Иена: <b>{currencies['currencies']['JPY']}</b> ₽\n' \
                                               f'🇨🇳 Китайский Юань: <b>{currencies['currencies']['CNY']}</b> ₽\n')
    except Exception as e:
        for admin in admin_ids:
            await bot.send_message(chat_id=admin, text=f'Ошибка при обновлении курса валют: {e}')
