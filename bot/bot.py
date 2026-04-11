import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (BotCommandScopeAllGroupChats,
                           BotCommandScopeAllPrivateChats)
from dotenv import load_dotenv

load_dotenv('.env')

from common.bot_cmds import BOT_CMDS_GROUP, BOT_CMDS_PRIVATE  # noqa
from handlers import auth, cable, common, twist, work  # noqa

TOKEN = os.getenv("BOT_TOKEN")


async def main() -> None:
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # dp.include_routers(private_router)

    dp.include_router(auth.router)
    dp.include_router(common.router)
    dp.include_router(cable.router)
    dp.include_router(twist.router)
    dp.include_router(work.router)

    await bot.set_my_commands(commands=BOT_CMDS_PRIVATE,
                              scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=BOT_CMDS_GROUP,
                              scope=BotCommandScopeAllGroupChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
