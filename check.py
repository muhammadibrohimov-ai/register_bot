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
    
    users = database.get_data("SELECT * FROM users;")
    
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

def return_message_text(c:int, lang:str):

    match c:
        case 1:
            if lang == "uz":
                return "To'liq isminginzi kiritng (Ali Aliyev Alijon o'g'li (qizi)): "
            else:
                return "Enter your fullname (Ali Aliyev Alijon o'g'li (qizi)): "

        case 2:
            if lang == "uz":
                return "Ismingiz not'og'ri formatda kiritlgan ekan, qayta uruning (Ali Aliyev Alijon o'g'li (qizi)): "
            else:
                return "Your name name is not in the right format, retry again (Ali Aliyev Alijon o'g'li (qizi))!"

        case 3:
            if lang =="uz":
                return "Tug'ilgan yilingizni kiritng (1950-2025): "
            else:
                return "Enter your birth year (1950-2025):"

        case 4:
            if lang == 'uz':
                return "Yilingiz noto'gri formatda ekan (1950-2025): "

            else:
                return "Your birthdate is not in the right format, retry again (1950-2025): "

        case 5:
            if lang =="uz":
                return "Yashash manzilingizni kiriting: "
            else:
                return "Enter your address: "

        case 6:
            if lang=='uz':
                return "Address ni xato formatda kiritngiz , qayta urining!"
            else:
                return "Address is not in the right format, retry again!"

        case 7:
            if lang == 'uz':
                return "Emailnigizni kiriting: "
            else:
                return "Enter your email: "
            
        case 8:
            if lang == 'uz':
                return "Email to'g'ri formatda emas, yoki allaqachon foydalanilgan, qayta urining!"
            else:
                return "Email is not in the right format or already used, retry again!"
            
        case 9:
            if lang =="uz":
                return 'Parol yarating: '
            else:
                return  "Create password: "
            
        case 10:
            if lang =="uz":
                return "Jo'natish"
            else:
                return "Send"
            
        case 11:
            if lang == 'uz':
                return "Parolingiz bizning talabimizga mos kelmadi, qayta urining!"
            else:
                return "Your paswwrod is not secure as we wanted, retry again!"
            
        case 12:
            if lang == 'uz':
                return "Telefon raqamingizni jo'nating: "
            else:
                return "Send your phone number: "
            
        case 13:
            if lang == 'uz':
                return 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!'
            else:
                return "You have signed up sucessfully!"
        
        case 14:
            if lang == 'uz':
                return 'Registratsiyada nimadur xato ketdi, iltimos qayta urining!'
            else:
                return "Something went wrong wiht registration, please try again!"    
            
        
def check_is_registered(data):
    print(data)
    return database.register_user(data)

    
    
            
def return_user_info(data:dict) -> str:
    
    info = ''
    for key, value in data.items():
        info += f'{key} - {value}\n'
        
    return info

def check_user(id):
    users = database.return_users()
    
    for user in users:
        if user[1] == id:
            return True
        
    return False