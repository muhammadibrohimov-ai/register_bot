import asyncio
import sqlite3 as sql


def get_ceonnection():
    return sql.connect("bot.db")

def create_table():
    with get_ceonnection() as db:
        dbc = db.cursor()
        query = '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INT NOT NULL UNIQUE,
            fullname VARCHAR(150) NOT NULL,
            year INT,
            address VARCHAR(150),
            email VARCHAR(150) NOT NULL,
            password VARCHAR(20) NOT NULL,
            phone_number VARCHAR(30)
        );
        '''
        dbc.execute(query)
        db.commit()
        
def register_user(data: dict) -> bool:
    create_table()
    
    keys = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))   
    values = tuple(data.values())               

    query = f"INSERT INTO users ({keys}) VALUES ({placeholders});"
    
    try:
        with get_ceonnection() as db:
            dbc = db.cursor()
            dbc.execute(query, values)
            db.commit()
        return True            
    except Exception as e:
        print("Xato:", e)
        return False

    
def return_users():
    create_table()
    
    try:
        with get_ceonnection() as db:
            dbc = db.cursor()
            
            dbc.execute("SELECT * FROM users;")
            
            data = dbc.fetchall()
            
            if not data:
                return []
            else:
                return data
        
    except:
        return []
    
def get_data(query):
    create_table()
    try:
        with get_ceonnection() as db:
            dbc = db.cursor()
            
            dbc.execute(query)
            
            data = dbc.fetchall()
            
            if not data:
                return []
            else:
                return data
        
    except:
        return []
    
