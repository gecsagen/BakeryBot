"""Клиентские диспетчеры"""
from aiogram import types, Dispatcher
from keyboards import client_keyboards


async def commands_start(message: types.Message):
    """Приветственный хендлер для команд start и help"""
    #  отдаем клавиатуру при команде /start или /help
    await message.answer('Привет! Это бот завьяловской пекарни:)', reply_markup=client_keyboards.kb_client)


def register_handlers_client(dp: Dispatcher):
    """
        Функция регистратор клиентских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(commands_start, commands=['start', 'help'])
