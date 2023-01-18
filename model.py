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
	id INTEGER NOT NULL UNIQUE,
	operator TEXT NOT NULL,
	date TEXT NOT NULL,
	time_msk TEXT NOT NULL,
	time_local TEXT NOT NULL,
	shop_name TEXT NOT NULL,
	passage	TEXT NOT NULL,
	ss_path	TEXT NOT NULL,
	PRIMARY KEY(id AUTOINCREMENT)
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


def make_screenshot_name(work_dir, difference, operator, shop_name, passage):
    today = datetime.date.today()
    dif = datetime.timedelta(hours=difference)
    time_msk = datetime.datetime.now()
    time_local = time_msk + dif
    time = (str(time_local).replace(':', '.'))
    result = f'{work_dir}/{time}.jpg'
    if not add_note(operator, today, time_msk, time_local,
                    shop_name, passage, result):
        return False
    return result


def add_note(operator, date, time_msk, time_local, shop_name, passage, path):
    try:
        ss_path = path.replace('/', '\\')
        ss_path = f'\\{ss_path}'
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""
                    INSERT INTO notes (operator, date, time_msk, time_local, shop_name, passage, ss_path)
                    VALUES ('{operator}',
                    '{date}',
                    '{time_msk}',
                    '{time_local}',
                    '{shop_name}',
                    '{passage}',
                    '{ss_path}'
                    )
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
# print(find_time_difference('945 Хабаровск 2 (город)'))
