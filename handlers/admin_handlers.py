"""Админские диспетчеры"""
from aiogram import types, Dispatcher
from loader import admins
from keyboards.admin_keyboards import kb_admin
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMProduct(StatesGroup):
    """Класс машины состояний для добавления товаров"""
    photo = State()  # состояние для фотографии
    name = State()  # состояние для имени
    description = State()  # состояние для описания
    price = State()  # состояние для цены


async def cm_start(message: types.Message):
    """Отправляет админское меню администратору"""
    if str(message.from_user.id) in admins:
        await message.reply('Привет, админ :D', reply_markup=kb_admin)


def register_handlers_admin(dp: Dispatcher):
    """
        Функция регистратор админских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(cm_start, commands=['админ'])
