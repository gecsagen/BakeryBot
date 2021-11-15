"""Админские клавиатуры"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#  создаем кнопки
button_add_product = KeyboardButton('Добавить продукт🍞')
button_add_gallery = KeyboardButton('Добавить в галерею🌅')
button_del_product = KeyboardButton('Удалить продукт❌')
button_del_gallery = KeyboardButton('Удалить из галереи❌')
button_load_timetable = KeyboardButton('Загрузить расписание🗒')
#  создаем клавиатуру из кнопок вместо обычной
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

#  добавляем кнопки на клавиатуру в строку
kb_admin.row(button_add_product, button_del_product).row(button_add_gallery, button_del_gallery) \
    .add(button_load_timetable)

#  callback кнопки для категорий продукции
kb_category = InlineKeyboardMarkup().add(InlineKeyboardButton('Хлеб🍞', callback_data='bread')). \
    add(InlineKeyboardButton('Булочки🍪', callback_data='buns')). \
    add(InlineKeyboardButton('Прочее❓', callback_data='other'))

kb_category_for_del_product = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Хлеб🍞', callback_data='choice_category bread')). \
    add(InlineKeyboardButton('Булочки🍪', callback_data='choice_category buns')). \
    add(InlineKeyboardButton('Прочее❓', callback_data='choice_category other'))
