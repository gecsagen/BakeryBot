"""Файл конфигурации для загрузки значений из переменного окружения"""
import os

token = os.getenv('TOKEN')  # токен бота
admins = os.getenv('ADMINS').split('$')  # список админов бота
address = os.getenv('ADDRESS').encode('IBM437').decode('utf-8').split('$')  # адрес организации
phones = os.getenv('PHONES').split('$')  # номера телефонов
names = os.getenv('NAMES').encode('IBM437').decode('utf-8').split('$')  # имена
email = os.getenv('EMAIL').encode('IBM437').decode('utf-8')  # email организации
