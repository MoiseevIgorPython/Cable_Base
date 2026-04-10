from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv

from api.client import auth_func
from common.states import AuthState, BaseState
from filters.chat_type_filter import ChatTypeFilter
from keyboards.reply_kbds import start_kdbs

load_dotenv(".env")

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(AuthState.username)
async def command_login(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(AuthState.password)
    await message.answer("Введите пароль.")


@router.message(AuthState.password)
async def command_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    auth_data = await state.get_data()
    token = await auth_func(auth_data)
    if token:
        await state.update_data(access_token=token["access_token"])
        await message.answer('Вы аутентифицированы! Что будете производить?',
                             reply_markup=start_kdbs)
        await state.set_state(BaseState.choose_work)
    else:
        await message.answer("Ошибка аутентификации.")
        await state.clear()
