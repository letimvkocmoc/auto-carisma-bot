import asyncio
import logging

import handlers
from aiogram import Bot, Dispatcher


logging.basicConfig(level=logging.INFO)

bot = Bot(token="6978793993:AAEK4exgYl6iTRr50qinGz9ScGaULdvL1tU")

dp = Dispatcher()

dp.include_router(handlers.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
