"""Админские диспетчеры"""
from aiogram import types, Dispatcher
from loader import admins
from keyboards.admin_keyboards import kb_admin, kb_category, kb_category_for_del_product
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import bot
from data import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMProduct(StatesGroup):
    """Класс машины состояний для добавления товаров"""
    category = State()  # состояние для категории
    photo = State()  # состояние для фотографии
    name = State()  # состояние для имени
    description = State()  # состояние для описания
    price = State()  # состояние для цены


class FSMGallery(StatesGroup):
    """Класс машины состояний для добавления в галерею"""
    photo = State()  # состояние для фотографии
    description = State()  # состояние для описания


class FSMTimetable(StatesGroup):
    """Класс машинны состояний для загрузки расписания"""
    photo = State()  # состояние для фотографии


async def cm_start(message: types.Message):
    """Отправляет админское меню администратору"""
    if str(message.from_user.id) in admins:
        await message.reply('Привет, админ :D', reply_markup=kb_admin)


async def cancel_handler(message: types.Message, state: FSMContext):
    """Выход из машины состояния если пользователь передумал"""
    if str(message.from_user.id) in admins:
        current_state = await state.get_state()  # узнаем текущее состояние
        #  если  не находимся в машине состояние ни чего не делаем
        if current_state is None:
            return
        #  иначе завершаем машину состояния
        await state.finish()
        await message.reply('Вы отменили действие')


async def add_new_product(message: types.Message):
    """Запускает процесс добавления нового товара в БД"""
    if str(message.from_user.id) in admins:
        await FSMProduct.category.set()
        await message.reply('Выберите пожалуйста категорию⬇️', reply_markup=kb_category)


async def callback_add_new_product(callback_query: types.CallbackQuery, state: FSMContext):
    """Функция для выяснения в какую категорию вносить изменения"""
    global category
    category = callback_query.data
    async with state.proxy() as data:
        data['category'] = category
    await FSMProduct.next()
    await bot.send_message(chat_id=callback_query.from_user.id, text='Теперь отправьте фото⬇️')


async def load_photo(message: types.Message, state: FSMContext):
    """Ловит фото продукта"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMProduct.next()
        await message.reply('Теперь введите название⬇️')


async def load_name(message: types.Message, state: FSMContext):
    """Ловит название продукта"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMProduct.next()
        await message.reply('Введи описание⬇️')


async def load_description(message: types.Message, state: FSMContext):
    """Ловит описание продукта"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMProduct.next()
        await message.reply('Теперь укажи цену⬇️')


async def load_price(message: types.Message, state: FSMContext):
    """Ловит цену продукта"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        #  вызываем функцию сохранения данных в БД
        await sqlite_db.sql_add_product(state)
        await message.answer('Продукт успешно добавлен!')
        await state.finish()


async def add_item_gallery(message: types.Message):
    """Запускает процесс добавления новой фото в БД"""
    if str(message.from_user.id) in admins:
        await FSMGallery.photo.set()
        await message.reply('Отправьте, фото⬇')


async def load_photo_gallery(message: types.Message, state: FSMContext):
    """Ловит фото продукта"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMGallery.next()
        await message.reply('Теперь введите описание⬇️')


async def load_description_gallery(message: types.Message, state: FSMContext):
    """Ловит описание для фото из галереи"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['description'] = message.text
        await sqlite_db.sql_add_new_item_in_gallery(state)
        await message.answer('Фото добавлено в галерею')
        await state.finish()


async def callback_del_gallery(callback_query: types.CallbackQuery):
    """Функция запускает удаление из галереи"""
    await bot.send_message(chat_id=callback_query.from_user.id, text=f'{callback_query.data}')
    await sqlite_db.sql_delete_from_gallery(callback_query.data.replace('del ', ''))
    await callback_query.answer(text='Запись удалена.', show_alert=True)


async def delete_item_gallery(message: types.Message):
    """Хендлер для команды удалить из галереи"""
    if str(message.from_user.id) in admins:
        read = await sqlite_db.sql_loads_all_gallery()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n')
            await bot.send_message(message.from_user.id, text='⬇⬇⬇', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Удалить❌', callback_data=f'del {ret[1]}')))


#  ----------------------------------------------------------------------------------------------------------------------


async def delete_product(message: types.Message):
    """Хендлер для команды удалить продукт"""
    if str(message.from_user.id) in admins:
        await message.reply('Выберите пожалуйста категорию⬇️', reply_markup=kb_category_for_del_product)


async def show_all_products_from_category_for_del(callback_query: types.CallbackQuery):
    """
        Хендлер для отображения всех продуктов из выбранной
        категории, с кнойкой 'удалить' под каждым продуктом
    """
    global category_del_product
    category_del_product = callback_query.data.replace('choice_category ', '')
    read = await sqlite_db.sql_loads_all_products_from_category(category_del_product)
    for ret in read:
        await bot.send_photo(callback_query.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        await bot.send_message(callback_query.from_user.id, text='⬇⬇⬇', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del_product {ret[1]}')))


async def delete_product_from_database(callback_query: types.CallbackQuery):
    """Срабатывает на кнопку удалить, и удаляет соответствующий продукт из БД"""
    data = callback_query.data.replace('del_product ', '')
    await bot.send_message(callback_query.from_user.id, data)
    await bot.send_message(callback_query.from_user.id, category_del_product)
    await sqlite_db.sql_delete_product(data, category_del_product)


#  ----------------------------------------------------------------------------------------------------------------------


async def add_new_timetable(message: types.Message):
    """Хендлер для команды 'Загрузить расписание'"""
    if str(message.from_user.id) in admins:
        await FSMTimetable.photo.set()
        await message.reply('Загрузите фото расписания⬇️')


async def load_photo_timetable(message: types.Message, state: FSMContext):
    """Ловит фото продукта"""
    if str(message.from_user.id) in admins:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await sqlite_db.sql_add_new_item_in_timetable(state)
        await message.answer('Расписание успешно загружено!')
        await state.finish()


#  ----------------------------------------------------------------------------------------------------------------------

def register_handlers_admin(dp: Dispatcher):
    """
        Функция регистратор админских диспетчеров, вызывается из main.py
    """
    dp.register_message_handler(cm_start, commands=['админ'])
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(add_new_product, Text(startswith=['Добавить продукт']), state=None)
    dp.register_callback_query_handler(callback_add_new_product,
                                       lambda x: x.data == 'bread' or x.data == 'buns' or x.data == 'other',
                                       state=FSMProduct.category)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMProduct.photo)
    dp.register_message_handler(load_name, state=FSMProduct.name)
    dp.register_message_handler(load_description, state=FSMProduct.description)
    dp.register_message_handler(load_price, state=FSMProduct.price)
    dp.register_message_handler(add_item_gallery, Text(startswith=['Добавить в галерею']), state=None)
    dp.register_message_handler(load_photo_gallery, content_types=['photo'], state=FSMGallery.photo)
    dp.register_message_handler(load_description_gallery, state=FSMGallery.description)
    dp.register_callback_query_handler(callback_del_gallery, lambda x: x.data.startswith('del '))
    dp.register_message_handler(delete_item_gallery, Text(startswith=['Удалить из галереи']))
    dp.register_message_handler(delete_product, Text(startswith=['Удалить продукт']))
    dp.register_callback_query_handler(show_all_products_from_category_for_del,
                                       lambda x: x.data.startswith('choice_category'))
    dp.register_callback_query_handler(delete_product_from_database,
                                       lambda x: x.data.startswith('del_product'))
    dp.register_message_handler(add_new_timetable, Text(startswith=['Загрузить расписание']), state=None)
    dp.register_message_handler(load_photo_timetable, content_types=['photo'], state=FSMTimetable.photo)
