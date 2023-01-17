import sqlite3 as sq
import os
import datetime
import openpyxl


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


def import_shops():
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = """
            DELETE FROM shops
        """
        cursor.execute(query)
        wb = openpyxl.load_workbook('shops.xlsx')  # подключение листа Excel
        sheet = wb.active
        # range(len(sheet["A"]) - 1)
        for i in range(len(sheet["A"])):
            if sheet['A'][i].value:
                query = f""" 
                    INSERT INTO shops (pid, shop_name) 
                    VALUES ('{sheet['A'][i].value}',
                    '{sheet['B'][i].value}')
                """
                cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as exc:
        print(exc)
        conn.close()
        return False


# create_db()
# print(import_shops())
