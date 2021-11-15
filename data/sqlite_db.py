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


async def sql_add_product(state):
    """Функция добавления новой продукта в выбранную категорию"""
    async with state.proxy() as data:
        cur.execute(f'INSERT INTO {data["category"]} VALUES (?, ?, ?, ?)', tuple(data.values())[1:])
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


async def sql_loads_all_buns():
    """Возвращает все продукты из категории булочки которые есть в бд"""
    return cur.execute('SELECT * FROM buns').fetchall()


async def sql_loads_all_other():
    """Возвращает все продукты из категории прочее которые есть в бд"""
    return cur.execute('SELECT * FROM other').fetchall()


async def sql_loads_all_gallery():
    """Возвращает все значения из галереи которые есть в бд"""
    return cur.execute('SELECT * FROM gallery').fetchall()


async def sql_loads_last_timetable():
    """Возвращает актуальное расписание из бд"""
    return cur.execute('SELECT * FROM timetable').fetchall()[-1]


async def sql_delete_bread(data):
    """Удаление хлеба из БД"""
    cur.execute('DELETE FROM bread WHERE name == ?', (data,))
    base.commit()


async def sql_delete_buns(data):
    """Удаление булочки из БД"""
    cur.execute('DELETE FROM buns WHERE name == ?', (data,))
    base.commit()


async def sql_delete_other(data):
    """Удаление элемента из категории 'прочее' из БД"""
    cur.execute('DELETE FROM other WHERE name == ?', (data,))
    base.commit()


async def sql_delete_from_gallery(description):
    """Удаление элемента из галереи"""
    cur.execute('DELETE FROM gallery WHERE description == ?', (description,))
    base.commit()
