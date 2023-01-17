import sqlite3 as sq
import os
import datetime
import openpyxl


def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS shops (
        shop_name TEXT NOT NULL UNIQUE,
        time_difference INTEGER
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
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""SELECT * FROM shops"""
        cursor.execute(query)
        shops = cursor.fetchall()
        conn.close()
        result = []
        for shop in shops:
            result.append(f'{str(shop[0])}')
        return result
    except Exception as exc:
        print(exc)
        conn.close()
        return False


def get_operators():
    try:
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
    except Exception as exc:
        print(exc)
        conn.close()
        return False


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
        for i in range(1, len(sheet["A"])):
            if sheet['A'][i].value:
                query = f"""
                    INSERT INTO shops (shop_name, time_difference)
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


def find_time_difference(shop):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""SELECT time_difference FROM shops
                    WHERE shop_name ='{shop}'"""
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return int(result[0][0])
    except Exception as exc:
        print(exc)
        conn.close()
        return False


def make_screenshot_name(work_dir, difference):
    dif = datetime.timedelta(hours=difference)
    now = datetime.datetime.now() + dif
    time = (str(now).replace(':', '.'))
    result = f'{work_dir}/{time}.jpg'
    return result


def add_note():
    pass


# create_db()
# print(import_shops())
# print(find_time_difference('945 Хабаровск 2 (город)'))
