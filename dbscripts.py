import sqlite3 as sq


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


def add_note():
    pass


create_db()
