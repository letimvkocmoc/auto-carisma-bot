import asyncio
import logging
import os

from core import handlers
from aiogram import Bot, Dispatcher
from keyboards.menu import set_menu
from database.utils import SQL
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.jobs import get_currency_rate


logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('BOT_TOKEN')
bot = Bot(token=bot_token)

dp = Dispatcher()

dp.include_router(handlers.router)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(get_currency_rate, trigger='cron', hour=10, minute=0, id='currency_update_10', kwargs={'bot': bot})
scheduler.add_job(get_currency_rate, trigger='cron', hour=18, minute=0, id='currency_update_18', kwargs={'bot': bot})


async def main():
    sql = SQL()
    scheduler.start()
    await set_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
