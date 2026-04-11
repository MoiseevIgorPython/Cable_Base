from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from common.states import AuthState, BaseState
from filters.chat_type_filter import ChatTypeFilter
from keyboards.reply_kbds import start_kdbs

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(Command("about"))
async def menu_cmd(message: Message):
    await message.answer("Я предоставляю информацию о кабеле и других комплектующих.")


@router.message(Command("stop"))
async def stop_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Бот остановлен", reply_markup=ReplyKeyboardRemove())


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AuthState.username)
    await message.answer("Бот запущен", reply_markup=ReplyKeyboardRemove())
    await message.answer("Введите почту.")


@router.message(lambda message: message.text == "Сначала")
async def restart_cmd(message: Message, state: FSMContext):
    user_data = await state.get_data()
    access_token = user_data.get("access_token")
    username = user_data.get("username")  # описать проверку действительности токена (запрос к api/users/me)
    await state.clear()
    if access_token:
        await state.update_data(
            access_token=access_token,
            username=username)
    await state.set_state(BaseState.choose_work)
    await message.answer("Что будете производить.", reply_markup=start_kdbs)
