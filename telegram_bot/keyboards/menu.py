from aiogram import Bot
from aiogram.types import BotCommand


async def set_menu(bot: Bot):

    main_menu_commands = [BotCommand(
        command='start',
        description='Запуск / обновление бота'
    )]
    await bot.set_my_commands(main_menu_commands)



