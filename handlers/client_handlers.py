"""Клиентские диспетчеры"""
from aiogram import types, Dispatcher
from keyboards import client_keyboards
from aiogram.dispatcher.filters import Text


async def commands_start(message: types.Message):
    """Приветственный хендлер для команд start и help"""
    #  отдаем клавиатуру при команде /start или /help
    await message.answer('Привет! Это бот завьяловской пекарни:)', reply_markup=client_keyboards.kb_client)


async def load_address(message: types.Message):
    """Хендлер для отображения адреса пекарни"""
    await message.reply('Омская обл, Знаменский Р-н, с.Завьялово, ул.Комарова 25')
    await message.answer_location(57.148317, 73.436807)


def register_handlers_client(dp: Dispatcher):
    """
        Функция регистратор клиентских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(load_address, Text(startswith='Адрес'))
