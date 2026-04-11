import os

import aiohttp
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from api.client import get_headers
from common.states import ArticleState, BaseState, ShellIsolateState
from dotenv import load_dotenv
from filters.chat_type_filter import ChatTypeFilter
from keyboards.reply_kbds import kdbs_from_data, restart_kbds, start_kdbs

load_dotenv(".env")

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(ShellIsolateState.construction)
async def select_construction(message: Message, state: FSMContext):
    await state.update_data(construction=message.text)
    await state.set_state(ShellIsolateState.title)
    state_data = await state.get_data()
    headers = await get_headers(state)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/cable/',
                               headers=headers,
                               params=state_data) as response:
            if response.status == 200:
                data = await response.json()
                if data == []:
                    current_data = await state.get_data()
                    current_data.pop("construction", None)
                    await state.set_data(current_data)
                    await state.set_state(ShellIsolateState.construction)
                    await message.answer("По данной конструкции кабелей не найдено.")
                    await message.answer("Выберите другую конструкцию.")
                else:
                    await message.answer("Выберите жилу.",
                                         reply_markup=kdbs_from_data(data, 'title'))
            else:
                await state.set_state(BaseState.choose_work)
                await message.answer("Ошибка получения данных с сервера.")
                await message.answer("Давайте с начала.",
                                     reply_markup=start_kdbs)


@router.message(ShellIsolateState.title)
async def select_core(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    state_data = await state.get_data()
    params = {
        "construction": state_data.get("construction"),
        "title": state_data.get("title")}
    headers = await get_headers(state)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/cable/',
                               headers=headers,
                               params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data == []:
                    await message.answer('Нет такого кабеля.')
                else:
                    response_text = (f"Параметры оболочки: \n"
                                     f"Артикул: {data[0]['article']} \n"
                                     f"Конструкция: {data[0]['construction']['name']} \n"
                                     f"Цвет: {data[0]['construction']['color']['name']} \n"
                                     f"Материал: {data[0]['construction']['shell_plastic']['name']} \n"
                                     f"Alumoflex: {data[0]['alumoflex']['name']} \n"
                                     f"Дреннажная жила: {data[0]['drennage']['name']} \n"
                                     f"Диаметр кабеля: {data[0]['outer_diametr']} \n"
                                     f"Диаметр в заготовке: {data[0]['inner_diametr']} \n"
                                     f"Радиальная толщина: {data[0]['construction']['radial_shell']} \n"
                                     f"\n"
                                     f"Параметры изоляции: \n"
                                     f"Диаметр изоляции: {data[0]['twisting']['diametr_wires'] + 2 * data[0]['construction']['radial_isolate']} \n"
                                     f"Диаметр жилы: {data[0]['twisting']['diametr_wires']} \n"
                                     f"Радиальная толщина: {data[0]['construction']['radial_isolate']} \n"
                                     f"Жила: {data[0]['twisting']['count_wires']} x {data[0]['twisting']['diametr_wires']} {data[0]['twisting']['metall']['name']} \n"
                                     f"Материал: {data[0]['construction']['shell_plastic']['name']} \n")
                    await message.answer(response_text,
                                         reply_markup=ReplyKeyboardRemove())
                await message.answer("Если хотите отправить другой запрос, нажмите Сначала.",
                                     reply_markup=restart_kbds)
            else:
                await message.answer("Ошибка получения данных с сервера.")
                await message.answer("Давайте с начала.",
                                     reply_markup=start_kdbs)


@router.message(ArticleState.article)
async def select_article(message: Message, state: FSMContext):
    await state.update_data(article=message.text)
    headers = await get_headers(state)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://{os.getenv("POSTGRES_HOST")}:8000/api/cable/{message.text}/',
                               headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                await message.answer(f"Ответ получен {data}") # отформатировать!!!!!!!!!!
                await message.answer("Если хотите отправить другой запрос, нажмите Сначала.",
                                     reply_markup=restart_kbds)
            else:
                await state.set_state(BaseState.choose_work)
                await message.answer("Ошибка получения данных с сервера.")
                await message.answer("Давайте с начала.",
                                     reply_markup=start_kdbs)
