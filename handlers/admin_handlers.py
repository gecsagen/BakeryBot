"""Админские диспетчеры"""
from aiogram import types, Dispatcher
from loader import admins
from keyboards.admin_keyboards import kb_admin, kb_category
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


class FSMProduct(StatesGroup):
    """Класс машины состояний для добавления товаров"""
    category = State()  # состояние для категории
    photo = State()  # состояние для фотографии
    name = State()  # состояние для имени
    description = State()  # состояние для описания
    price = State()  # состояние для цены


async def cm_start(message: types.Message):
    """Отправляет админское меню администратору"""
    if str(message.from_user.id) in admins:
        await message.reply('Привет, админ :D', reply_markup=kb_admin)


async def add_new_product(message: types.Message):
    """Запускает процесс добавления нового товара в БД"""
    if str(message.from_user.id) in admins:
        await message.reply('Выберите пожалуйста категорию:', reply_markup=kb_category)


async def callback_add_new_product(callback_query: types.CallbackQuery):
    """Функция для выяснения в какую категорию вносить изменения"""
    global category
    category = callback_query.data


def register_handlers_admin(dp: Dispatcher):
    """
        Функция регистратор админских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(cm_start, commands=['админ'])
    dp.register_message_handler(add_new_product, Text(startswith=['Добавить продукт']))
    dp.register_callback_query_handler(callback_add_new_product,
                                       lambda x: x.data == 'bread' or x.data == 'buns' or x.data == 'other')
