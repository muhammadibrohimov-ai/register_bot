from outer import check

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

start_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="uz"), KeyboardButton(text='en')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Tanlang"
)


def return_phone(user_lang:str):
    return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=check.return_message_text(c=10, lang=user_lang), request_contact=True)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
                input_field_placeholder="Tanlang"
            )

time_uz = ['Oylik', 'Haftalik', 'Kunlik']    
time_en = ['Monthly', 'Weekly', 'Daily']

viloyatlar  = [
    "Andijon",
    "Buxoro",
    "Farg'ona",
    "Jizzax",
    "Namangan",
    "Qarshi",
    "Nukus",
    "Samarqand",
    "Guliston",
    "Termiz",
    "Toshkent"
]



async def return_times(lang:str):
    keyboard = ReplyKeyboardBuilder()
    
    if lang =='uz':
        
        for time in time_uz:
            keyboard.add(KeyboardButton(text=time))
        
    else:
        for time in time_en:
            keyboard.add(KeyboardButton(text=time))
            
            
    return keyboard.adjust(2).as_markup(resize_keyboard = True, input_field_placeholder="Tanlang")
    

async def return_regions(lang:str):
    keyboard = InlineKeyboardBuilder()
    
        
    for viloyat in viloyatlar:
        keyboard.add(InlineKeyboardButton(text=viloyat, callback_data=viloyat))
    
            
    return keyboard.adjust(2).as_markup()
