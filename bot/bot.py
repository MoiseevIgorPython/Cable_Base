import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import requests
from pprint import pprint
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
FASTAPI_URL = 'http://localhost:8000/api/components/alumoflex/'
BOT_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# from aiogram.types import ReplyKeyboardRemove
# await message.answer("Клавиатура удалена", reply_markup=ReplyKeyboardRemove())


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
# print(sys.stdlib_module_names)

@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    print(message)#.model_dump_json(indent=4, exclude_none=True))
    await message.answer('Угадывай!')




# @dp.message(CommandStart())
# async def command_start(message: Message) -> None:
#     pprint(dir(message))
#     button1 = KeyboardButton(text='Изоляцию')
#     button2 = KeyboardButton(text='Оболочку')
#     keyboard = ReplyKeyboardMarkup(keyboard=[[button1, button2]],
#                                    resize_keyboard=True)
#     await message.answer("Что производите?", reply_markup=keyboard)


# @dp.message((F.text == "Изоляцию") | (F.text == "Оболочку"))
# async def select_constr(message: Message, state: FSMContext) -> None:
#     await state.update_data(work_choice=message.text) # Сохраняем выбор Оболочку или Изоляцию
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://127.0.0.1:8000/api/construction/') as response:
#             if response.status == 200:
#                 buttons = []
#                 data = await response.json()
#                 for i in data:
#                     buttons.append(KeyboardButton(text=str(i['number'])))
#                 keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
#     await message.answer("Выберите конструкцию", reply_markup=keyboard)


# @dp.message()
# async def process_construction(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     work_choice = user_data.get('work_choice')
#     constr_choice = user_data.get('constr_choice')
#     if work_choice not in ["Изоляцию", "Оболочку"]:
#         await message.answer("Пожалуйста, сначала выберите Изоляцию или Оболочку.")
#         return
#     elif constr_choice is None and work_choice in ["Изоляцию", "Оболочку"]:
#         await state.update_data(constr_choice=message.text)
#         async with aiohttp.ClientSession() as session:
#             async with session.get('http://127.0.0.1:8000/api/core/') as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     buttons = [KeyboardButton(text=str(i['name'])) for i in data]
#                     keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
#                     await message.answer('Выберите жилу', reply_markup=keyboard)
#                 else:
#                     await message.answer("Ошибка получения данных с сервера.")
#     elif constr_choice is not None:
#         # выполнить запрос к апи cable с параметрами конструкции и жилы
#         params = {'construction': int(constr_choice),
#                   'core': message.text}
#         async with aiohttp.ClientSession() as session:
#             async with session.get('http://127.0.0.1:8000/api/cable/') as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     result_data = [item for item in data if item['construction']['number'] == int(constr_choice) and item['core']['name'] == message.text]
#                     if work_choice == 'Изоляцию':
#                         response_data = (f'Ваша изоляция:\n'
#                                          f'Конструкция: K-{(result_data[0]['construction']['number'])} {result_data[0]['construction']['name']}\n'
#                                          f'Жила: {result_data[0]['core']['name']}{result_data[0]['core']['metall']['name']}\n'
#                                          f'Материал: сюда добавить материал изоляции\n'#{result_data[0]['construction']['plastic']['name']}\n'
#                                          f'Толщина оболочки: {result_data[0]['thickness_isolat']}\n'
#                                          f'Диаметр: {result_data[0]['diametr_isolate']}'
#                                          )
#                     if work_choice == 'Оболочку':
#                         response_data = (f'Ваша оболочка:\n'
#                                          f'Конструкция: K-{(result_data[0]['construction']['number'])} {result_data[0]['construction']['name']}\n'
#                                          f'Жила: {result_data[0]['core_rel']['name']}\n'
#                                          f'Материал: {result_data[0]['construction']['plastic']['name']}\n'
#                                          f'Толщина оболочки: {result_data[0]['thickness_shell']}\n'
#                                          f'Диаметр: {result_data[0]['diametr_shell']}'
#                                          )

#         await message.answer(response_data)






    # await state.clear()


# @dp.message()
# async def funk(message: Message, state: FSMContext):












async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
