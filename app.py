import logging
from loader import dp
from aiogram.utils import executor
from handlers import client_handlers, admin_handlers

# настройка логирования бота
logging.basicConfig(level=logging.DEBUG)


async def on_startup(_):
    """Выполняется самой первой при запуске бота"""
    print('Бот вышел в онлайн!')


#  запускаем функции регистрации хендлеров
client_handlers.register_handlers_client(dp)
admin_handlers.register_handlers_admin(dp)

#  запуск бота в режиме polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
