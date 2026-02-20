from aiogram.types import BotCommand

BOT_CMDS_PRIVATE = [
    BotCommand(command='start', description='Запуск бота'),
    BotCommand(command='about', description='Что делает бот'),
    BotCommand(command='stop', description='Остановить бота')
]

BOT_CMDS_GROUP = [
    BotCommand(command='about', description='Чем я тут занимаюсь?')
]
