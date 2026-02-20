import aiohttp
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from filters.chat_type_filter import ChatTypeFilter
from keyboards.reply_kbds import kdbs_from_data, start_kdbs

private_router = Router()
private_router.message.filter(ChatTypeFilter(['private']))


class BaseState(StatesGroup):
    choose_work = State()


class ShellIsolateState(BaseState):
    """Состояния при выборе Изоляции или Оболочки."""
    work = State()
    construction = State()
    core = State()


class TwistState(BaseState):
    """Состояния при выборе Скрутки"""
    work = State()
    metall = State()
    count_wires = State()
    diametr_wires = State()


@private_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(BaseState.choose_work)
    await message.answer("Бот запущен", reply_markup=ReplyKeyboardRemove())
    await message.answer("Что производите?", reply_markup=start_kdbs)


@private_router.message(Command("about"))
async def menu_cmd(message: Message):
    await message.answer("Я предоставляю информацию о кабеле и других комплектующих.")


@private_router.message(Command("stop"))
async def stop_cmd(message: Message): #сдесь необходимо сбросить состояние
    await message.answer("Бот остановлен", reply_markup=ReplyKeyboardRemove())


# =======================Выбрана "Изоляция" или "Оболочка"==============================

@private_router.message(BaseState.choose_work)
async def select_work(message: Message, state: FSMContext):
    if message.text in ['Изоляцию', 'Оболочку']:
        await state.update_data(work=message.text)
        await state.set_state(ShellIsolateState.construction)

        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/api/construction/') as response:
                if response.status == 200:
                    data = await response.json()
                    await message.answer('Выберите конструкцию.',
                                         reply_markup=kdbs_from_data(data, 'name'))
                else:
                    await message.answer("Ошибка получения данных с сервера.")
    elif message.text in ['Скрутку']:
        await state.update_data(work=message.text)
        await state.set_state(TwistState.metall)
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/api/components/metall/') as response:
                if response.status == 200:
                    data = await response.json()
                    await message.answer('Выберите металл.',
                                         reply_markup=kdbs_from_data(data, 'name'))
                else:
                    await message.answer("Ошибка получения данных с сервера.")


@private_router.message(ShellIsolateState.construction)
async def select_construction(message: Message, state: FSMContext):
    await state.update_data(construction=message.text)
    await state.set_state(ShellIsolateState.core)
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/isolation/') as response:
            if response.status == 200:
                data = await response.json()
            else:
                await message.answer("Ошибка получения данных с сервера.")
    await message.answer("Выберите жилу.", reply_markup=kdbs_from_data(data, 'core'))


@private_router.message(ShellIsolateState.core)
async def select_core(message: Message, state: FSMContext):
    await state.update_data(core=message.text)
    state_data = await state.get_data()
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/cable/',
                               params=state_data) as response:
            if response.status == 200:
                data = await response.json()
                response_text = (f"Параметры оболочки: \n"
                                 f"Артикул: {data[0]['article']} \n"
                                 f"Конструкция: {data[0]['construction']['name']} \n"
                                 f"Цвет: {data[0]['construction']['color']['name']} \n"
                                 f"Материал: {data[0]['construction']['shell_plastic']['name']} \n"
                                 f"Alumoflex: {data[0]['alumoflex']['name']} \n"
                                 f"Дреннажная жила: {data[0]['drennage']['name']} \n"
                                 f"Диаметр кабеля: {data[0]['outer_diametr']} \n"
                                 f"Диаметр в заготовке: {data[0]['inner_diametr']} \n"
                                 f"Радиальная толщина: {data[0]['radial']} \n"
                                 f"\n"
                                 f"Параметры изоляции"
                                 f"Диаметр изоляции: {data[0]['isolation']['outer_diametr']} \n"
                                 f"Диаметр жилы: {data[0]['isolation']['inner_diametr']} \n"
                                 f"Радиальная толщина: {data[0]['isolation']['radial']} \n"
                                 f"Жила: {data[0]['isolation']['core']} \n"
                                 f"Материал: {data[0]['construction']['isolate_plastic']['name']} \n")
                await message.answer(response_text,
                                     reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer("Ошибка получения данных с сервера.")
    await state.clear()


# =======================Выбрана "Скрутка"==============================


@private_router.message(TwistState.metall)
async def choise_metall(message: Message, state: FSMContext):
    await state.update_data(metall=message.text)
    await state.set_state(TwistState.count_wires)
    await message.answer("Введите количество жил.",
                         reply_markup=ReplyKeyboardRemove())


@private_router.message(TwistState.count_wires)
async def select_count_wires(message: Message, state: FSMContext):
    await state.update_data(count_wires=message.text)
    await state.set_state(TwistState.diametr_wires)
    await message.answer("Введите диаметр жилы.")


@private_router.message(TwistState.diametr_wires)
async def select_diametr_wires(message: Message, state: FSMContext):
    await state.update_data(diametr_wires=message.text)
    state_data = await state.get_data()
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/twist/',
                               params=state_data) as response:
            if response.status == 200:
                data = await response.json()
                response_text = (f"Параметры для Вашей работы: \n"
                                 f"Металл: {data[0]['metall']['name']} \n"
                                 f"Количество проволоки: {data[0]['count_wires']} \n"
                                 f"Диаметр проволоки: {data[0]['diametr_wires']} \n"
                                 f"Сопротивление: {data[0]['resistance']} \n"
                                 f"Шаг: {data[0]['step']}")
                await message.answer(response_text)
            else:
                await message.answer("Ошибка получения данных с сервера.")
    await state.clear()
