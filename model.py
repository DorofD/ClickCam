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

    query = """CREATE TABLE IF NOT EXISTS operations (
        note INTEGER NOT NULL UNIQUE,
        shop_name TEXT NOT NULL UNIQUE
    )
    """
    cursor.execute(query)

    conn.commit()
    conn.close()


def add_note(operator):
    today = datetime.date.today()
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


def boba(sas):
    print(sas)


create_db()
