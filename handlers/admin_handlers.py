"""Админские диспетчеры"""
from aiogram import types, Dispatcher
from loader import admins


async def cm_start(message: types.Message):
    """Отправляет админское меню администратору"""
    if str(message.from_user.id) in admins:
        await message.reply('Привет, админ :D')


def register_handlers_admin(dp: Dispatcher):
    """
        Функция регистратор админских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(cm_start, commands=['админ'])
