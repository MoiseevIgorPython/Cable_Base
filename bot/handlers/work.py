from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from api.client import get_constructions, get_headers, get_metall
from common.states import (ArticleState, BaseState, ShellIsolateState,
                           TwistState)
from dotenv import load_dotenv
from filters.chat_type_filter import ChatTypeFilter
from keyboards.reply_kbds import kdbs_from_data, start_kdbs

load_dotenv(".env")

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(BaseState.choose_work)
async def select_work(message: Message, state: FSMContext):
    headers = await get_headers(state)
    if message.text == 'Изоляцию/Оболочку':
        await state.update_data(work=message.text)
        await state.set_state(ShellIsolateState.construction)
        data = await get_constructions(headers)
        if data:
            await message.answer('Выберите конструкцию.',
                                 reply_markup=kdbs_from_data(data, 'name'))
            await message.answer("Vot inline klava", reply_markup=keyboard)
        else:
            await state.set_state(BaseState.choose_work)
            await message.answer("Ошибка получения данных с сервера.")
            await message.answer("Давайте с начала.",
                                 reply_markup=start_kdbs)

    elif message.text == 'Скрутку':
        await state.update_data(work=message.text)
        await state.set_state(TwistState.metall)

        data = await get_metall(headers)
        if data:
            await message.answer('Выберите металл.',
                                 reply_markup=kdbs_from_data(data, 'name'))
        else:
            await state.set_state(BaseState.choose_work)
            await message.answer("Ошибка получения данных с сервера.")
            await message.answer("Давайте с начала.",
                                 reply_markup=start_kdbs)

    elif message.text == 'Ввод артикула':
        await state.update_data(work=message.text)
        await state.set_state(ArticleState.article)
        await message.answer('Введите артикул:')
