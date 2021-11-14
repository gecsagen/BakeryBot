"""Модуль для работы с БД бота"""
import sqlite3 as sq


def sql_start():
    """
        Функция создания БД или подключение к ней
        если она уже создана
    """
    global base, cur
    #  подключение к БД
    base = sq.connect('bakery_db.db')
    #  курсор для взаимодействия с БД
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    #  создаем таблицы в БД, в которую будем вносить данные
    base.execute('CREATE TABLE IF NOT EXISTS bread(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT )')
    base.execute('CREATE TABLE IF NOT EXISTS buns(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT )')
    base.execute('CREATE TABLE IF NOT EXISTS other(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT )')
    base.execute('CREATE TABLE IF NOT EXISTS gallery(img TEXT, description TEXT PRIMARY KEY)')
    base.execute('CREATE TABLE IF NOT EXISTS timetable(img TEXT)')
    #  сохраняем изменения
    base.commit()
