"""Клиентские диспетчеры"""
from aiogram import types, Dispatcher
from keyboards import client_keyboards
from aiogram.dispatcher.filters import Text
from data import sqlite_db
from loader import bot
from data.config import address, phones, email, names


async def commands_start(message: types.Message):
    """Приветственный хендлер для команд start и help"""
    #  отдаем клавиатуру при команде /start или /help
    await message.answer('Привет! Это бот завьяловской пекарни:)', reply_markup=client_keyboards.kb_client)


async def load_address(message: types.Message):
    """Хендлер для отображения адреса пекарни"""
    await message.reply(address[0])
    await message.answer_location(float(address[1]), float(address[2]))


async def load_contacts(message: types.Message):
    """Хендлер для отображения контактов пекарни"""
    for name, phone in zip(names, phones):
        await message.answer_contact(phone_number=phone, first_name=name)
    await message.answer(email)


async def show_products(message: types.Message):
    """Хендлер для команды 'продукция' отображает категории продукции"""
    await message.reply('Выберите пожалуйста категорию⬇️', reply_markup=client_keyboards.kb_category_for_show)


async def show_all_products_from_category(callback_query: types.CallbackQuery):
    """Отображает все товары выбранной категории"""
    category = callback_query.data.replace('show ', '')
    read = await sqlite_db.sql_loads_all_products_from_category(category)
    for ret in read:
        await bot.send_photo(callback_query.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


async def show_all_photos_from_gallery(message: types.Message):
    """Хендлер для кнопки 'Галерея', отображает все фото из галереи"""
    read = await sqlite_db.sql_loads_all_gallery()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n')


def register_handlers_client(dp: Dispatcher):
    """
        Функция регистратор клиентских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(load_address, Text(startswith='Адрес'))
    dp.register_message_handler(load_contacts, Text(startswith='Контакты'))
    dp.register_message_handler(show_products, Text(startswith='Продукция'))
    dp.register_callback_query_handler(show_all_products_from_category, lambda x: x.data.startswith('show'))
    dp.register_message_handler(show_all_photos_from_gallery, Text(startswith='Галерея'))
