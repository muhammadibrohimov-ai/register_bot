import asyncio
from datetime import datetime as dt
import database

async def check_fullname(fullname: str):
    
    for i in fullname.lower():
        if not (i.isalpha() or i in ["'", "’", " "]):
            return False
    
    return False if len(fullname.split()) != 4 or not (fullname.endswith("qizi") or fullname.endswith("o'g'li") or fullname.endswith("o’g’li"))  else  True
        
async def check_year(year:str):
    year = int(year)
    return False if year<1950 or year>dt.now().year else True

async def check_address(address):
    
    return False if not address else True


async def check_email(email:str): # 5
    
    if not email.endswith(('@gmail.com', 'mail.ru', 'yahoo.com', 'yandex.com', 'yandex.ru')):
        return False
    
    if len(email.split("@")[0]) < 5:
        return False
    
    users = await database.get_data("SELECT * FROM users;")
    
    for user in users:
        if user[5] == email:
            return False
        
    return True


async def check_password(password:str):
    
    up, low, dig, punc = 0, 0, 0, 0
    
    for i in password:
        if i.isupper():
            up += 1
        elif i.islower():
            low += 1
        elif i.isdigit():
            dig += 1
        elif i == " ":
            return False
        else:
            punc+=1

    if len(password) >= 8 and up >= 1 and low >= 1 and dig >= 1 and punc >= 1:
        return True

    else:
        return False