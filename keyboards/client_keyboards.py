"""Пользовательские клавиатуры"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#  создаем кнопки
button_products = KeyboardButton('Продукция🍞')
button_gallery = KeyboardButton('Галерея🌅')
button_address = KeyboardButton('Адрес🗺')
button_contacts = KeyboardButton('Контакты📱')

#  создаем клавиатуру из кнопок вместо обычной
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

#  добавляем кнопки на клавиатуру в строку
kb_client.row(button_products, button_gallery).row(button_address, button_contacts)

#  callback кнопки для категорий продукции
kb_category_for_show = InlineKeyboardMarkup().add(InlineKeyboardButton('Хлеб🍞', callback_data='show bread')). \
    add(InlineKeyboardButton('Булочки🍪', callback_data='show buns')). \
    add(InlineKeyboardButton('Прочее❓', callback_data='show other'))
