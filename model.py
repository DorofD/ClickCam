import sqlite3 as sq
import os
import datetime
import openpyxl
import webbrowser


def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS shops (
        pid INTEGER UNIQUE,
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

    query = """CREATE TABLE IF NOT EXISTS cams (
    pid INTEGER,
    shop_name TEXT NOT NULL,
    passage TEXT,
    ip TEXT,
    login TEXT,
    password TEXT)
    """
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS problems(
    operator TEXT,
    time TEXT,
    shop TEXT,
    ip TEXT,
    description TEXT)
    """
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS intervals(
    operator TEXT,
    date TEXT,
    time_msk TEXT,
    time_local TEXT,
    shop TEXT,
    passage TEXT,
    status TEXT)
    """
    cursor.execute(query)

    conn.commit()
    conn.close()


def make_directory(operator, shop, passage):
    today = datetime.date.today()
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
            result.append(f'{str(shop[1])}')
        return result
    except Exception as exc:
        print(exc)
        conn.close()
        return False


def get_operator():
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""SELECT * FROM operators"""
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result[0][0]
    except Exception as exc:
        print(exc)
        conn.close()
        return 'Нет оператора'


def set_operator(operator):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = """
                DELETE FROM operators
            """
        cursor.execute(query)
        query = f"""
                INSERT INTO operators (username)
                VALUES ('{operator}')
            """
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
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
        for i in range(1, len(sheet["A"])):
            if sheet['A'][i].value:
                query = f"""
                    INSERT INTO shops (pid, shop_name, time_difference)
                    VALUES ('{sheet['A'][i].value}',
                    '{sheet['B'][i].value}',
                    '{sheet['C'][i].value}')
                """
                cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as exc:
        print(exc)
        conn.close()
        return False


def import_cams():
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = """
            DELETE FROM cams
        """
        cursor.execute(query)
        wb = openpyxl.load_workbook('cams.xlsx')  # подключение листа Excel
        sheet = wb.active
        for i in range(1, len(sheet["A"])):
            if sheet['A'][i].value:
                query = f"""
                    INSERT INTO cams (pid, shop_name, passage, ip, login, password)
                    VALUES ('{sheet['A'][i].value}',
                    '{sheet['B'][i].value}',
                    '{sheet['C'][i].value}',
                    '{sheet['D'][i].value}',
                    '{sheet['E'][i].value}',
                    '{sheet['F'][i].value}')
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


def make_record_name(work_dir, shop_name):
    time = (str(datetime.datetime.now()).replace(':', '.'))
    # result = f'{work_dir}/RECORD {shop_name} {time}.avi'
    result = f'{work_dir}/RECORD {shop_name} {time}.mp4'
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


def get_cam_connection(shop, passage):
    try:
        print(shop)
        print(passage)
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""SELECT ip, login, password FROM cams
                    WHERE shop_name ='{shop}' AND passage = '{passage}'"""
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result[0]
    except Exception as exc:
        print(exc)
        conn.close()
        return False


def open_camera(address):
    ie = webbrowser.get(
        'c:\\program files\\internet explorer\\iexplore.exe')
    ie.open(f'http://{address}', new=0)


def cam_problem_report(operator, shop, ip, description):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""
                INSERT INTO problems (operator, time, shop, ip, description)
                VALUES ('{operator}',
                '{str(datetime.datetime.now())}',
                '{shop}',
                '{ip}',
                '{description}'
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


def set_time_interval(operator, shop, passage, status, difference):
    try:
        today = datetime.date.today()
        dif = datetime.timedelta(hours=difference)
        time_msk = datetime.datetime.now()
        time_local = time_msk + dif
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""
                INSERT INTO intervals (operator, date, time_msk, time_local, shop, passage, status)
                VALUES ('{operator}',
                '{str(today)}',
                '{str(time_msk)}',
                '{str(time_local)}',
                '{shop}',
                '{passage}',
                '{status}'
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
# print(import_cams())
# add_opeartors()
# print(find_time_difference('945 Хабаровск 2 (город)'))

# get_cam_connection('Ханты-Мансийск (город)', '1')
