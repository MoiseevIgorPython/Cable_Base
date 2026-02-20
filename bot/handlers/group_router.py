from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from filters.chat_type_filter import ChatTypeFilter

group_router = Router()
group_router.message.filter(ChatTypeFilter(['group']))


@group_router.message(Command('about'))
async def about_cmd(message: Message):
    await message.reply('Я послежу чтобы вы не ругались!')
