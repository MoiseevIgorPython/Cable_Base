from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_kdbs = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изоляцию'),
            KeyboardButton(text='Оболочку'),
            KeyboardButton(text='Скрутку')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Текст в строке ввода.'
)


def kdbs_from_data(data: dict, field: str):
    """Формирование клавиатуры из полученных данных."""
    buttons = [KeyboardButton(text=str(data[i][f'{field}']))
               for i in range(len(data))]
    buttons = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True)
    return keyboard
