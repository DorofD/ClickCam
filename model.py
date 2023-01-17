import sqlite3 as sq
import os
import datetime


def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS shops ( 
        pid INTEGER NOT NULL UNIQUE,
        shop_name TEXT NOT NULL UNIQUE
    )
    """
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS operators (
        username TEXT NOT NULL UNIQUE
    )
    """
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS notes (
        note INTEGER NOT NULL UNIQUE,
        shop_name TEXT NOT NULL UNIQUE
    )
    """
    cursor.execute(query)

    conn.commit()
    conn.close()


def add_note(operator):
    pass


def make_directory(operator, shop, passage):
    today = datetime.date.today()
    # print(operator)
    # print(shop)
    # print(passage)
    if not os.path.exists(f'screenshots/{operator}/{today}/{shop}/Проход {passage}'):
        os.makedirs(f'screenshots/{operator}/{today}/{shop}/Проход {passage}')
    result = f'screenshots/{operator}/{today}/{shop}/Проход {passage}'
    return result


def get_shops():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM shops"""
    cursor.execute(query)
    shops = cursor.fetchall()
    conn.close()
    result = []
    for shop in shops:
        result.append(f'{str(shop[0])} {str(shop[1])}')
    print('GET SHOPS')
    return result


def get_operators():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM operators"""
    cursor.execute(query)
    operators = cursor.fetchall()
    conn.close()
    result = []
    for operator in operators:
        result.append(str(operator[0]))
    return result
# create_db()
# for b in a:
#     print(f'{str(b[0])} {str(b[1])}')


print(get_operators())
