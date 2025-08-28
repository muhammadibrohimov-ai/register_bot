import asyncio
import sqlite3 as sql

def get_connetion():
    return sql.connect("register_bot.db")

async def create_table_users():
    with get_connetion() as db:
        dbc = db.cursor()

        query = f'''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            fullname VARCHAR(150) NOT NULL,
            year INTEGER,
            phone_number VARCHAR(50),
            address VARCHAR(150),
            email VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
        '''
        dbc.execute(query)
        db.commit()

async def get_data(query):
    try:
        query.lower().startswith("select")
        with get_connetion() as db:
            dbc = db.cursor()
            dbc.execute(query)
            data = dbc.fetchall()

    except:
        data = []

    return data