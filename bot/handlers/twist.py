from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from dotenv import load_dotenv

from api.client import get_headers, get_twist
from common.states import TwistState
from filters.chat_type_filter import ChatTypeFilter
from keyboards.reply_kbds import restart_kbds

load_dotenv(".env")

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(TwistState.metall)
async def choise_metall(message: Message, state: FSMContext):
    await state.update_data(metall=message.text)
    await state.set_state(TwistState.count_wires)
    await message.answer("Введите количество жил.",
                         reply_markup=ReplyKeyboardRemove())


@router.message(TwistState.count_wires)
async def select_count_wires(message: Message, state: FSMContext):
    await state.update_data(count_wires=message.text)
    await state.set_state(TwistState.diametr_wires)
    await message.answer("Введите диаметр жилы.")


@router.message(TwistState.diametr_wires)
async def select_diametr_wires(message: Message, state: FSMContext):
    headers = await get_headers(state)
    await state.update_data(diametr_wires=message.text)
    state_data = await state.get_data()
    params = {
        "count_wires": state_data["count_wires"],
        "diametr_wires": state_data["diametr_wires"],
        "metall": state_data["metall"]
    }
    data = await get_twist(headers, params)
    if not data:
        await message.answer("Нет такой жилы, попробуйте еще раз.")
        await message.answer("Что будете производить?",
                             reply_markup=restart_kbds)
    else:
        response_text = (f"Параметры для Вашей работы: \n"
                         f"Металл: {data[0]['metall']['name']} \n"
                         f"Количество проволоки: {data[0]['count_wires']} \n"
                         f"Диаметр проволоки: {data[0]['diametr_wires']} \n"
                         f"Сопротивление: {data[0]['resistance']} \n"
                         f"Шаг: {data[0]['step']}")
        await message.answer(response_text)
        await message.answer("Если хотите отправить другой запрос нажмите Сначала.",
                             reply_markup=restart_kbds)
