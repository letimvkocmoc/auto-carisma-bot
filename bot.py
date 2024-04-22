import asyncio
import logging
import os

import handlers
from aiogram import Bot, Dispatcher
from keyboards.menu import set_menu
from database.utils import SQL


logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('BOT_TOKEN')
bot = Bot(token=bot_token)

dp = Dispatcher()

dp.include_router(handlers.router)


async def main():
    sql = SQL()
    await set_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
