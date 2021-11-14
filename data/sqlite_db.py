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


async def sql_add_product_in_bread(state):
    """Функция добавления новой продукта в категорию 'Хлеб'"""
    async with state.proxy() as data:
        cur.execute('INSERT INTO bread VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_product_in_buns(state):
    """Функция добавления новой продукта в категорию 'Булочки'"""
    async with state.proxy() as data:
        cur.execute('INSERT INTO buns VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_product_in_other(state):
    """Функция добавления нового продукта в категорию 'Прочее'"""
    async with state.proxy() as data:
        cur.execute('INSERT INTO other VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_new_item_in_gallery(state):
    """Функция добавления новой картинки в галерею"""
    async with state.proxy() as data:
        cur.execute('INSERT INTO gallery VALUES (?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_new_item_in_timetable(state):
    """Функция добавления нового расписания"""
    async with state.proxy() as data:
        cur.execute('INSERT INTO timetable VALUES (?,)', tuple(data.values()))
        base.commit()


async def sql_loads_all_breads():
    """Возвращает все продукты из категории хлеб которые есть в бд"""
    return cur.execute('SELECT * FROM bread').fetchall()
