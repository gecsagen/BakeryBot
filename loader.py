"""
    Обекты бота и диспетчера создаются в этом файле, чтобы
    удобно их импортировать из любого места проекта
"""
from data.config import token
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#  создаем хранилище в оперативной памяти
storage = MemoryStorage()

#  создаем бот, считав ключ API из переменного окружения
bot = Bot(token=token)

#  создаем дистпетчер
dp = Dispatcher(bot, storage=storage)
