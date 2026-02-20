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

from common.bot_cmds import BOT_CMDS_GROUP, BOT_CMDS_PRIVATE
from handlers.group_router import group_router
from handlers.private_router import private_router

TOKEN = os.getenv("BOT_TOKEN")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(private_router, group_router)

    await bot.set_my_commands(commands=BOT_CMDS_PRIVATE,
                              scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=BOT_CMDS_GROUP,
                              scope=BotCommandScopeAllGroupChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
