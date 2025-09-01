from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import database
import check

router = Router()

# Keyboards

start_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="uz"), KeyboardButton(text='en')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Finite State Machine subclass

class Register(StatesGroup):
    fullname = State()
    year = State()
    address = State()
    email = State()
    password = State()

user_lang = 'uz'

@router.message(CommandStart())
async def cmd_start(message: Message, state:FSMContext):
    global current_user
    current_user = message.from_user
    await state.set_state(Register.fullname)
    await message.answer(
        text="Namoz vaqtlari botga xush kelibsiz!\nWelcome to the prayer times bot\n\nTilni kiritng:\nChoose the language: ",
        reply_markup=start_keyboards
    )

@router.message(F.text=='en')
@router.message(F.text=='uz')
async def register_uz(message:Message, state:FSMContext):

    global user_lang
    
    if not message.text == "uz":
        user_lang = "en"


    status = check.check_user(current_user.id)
    
    if  status:
    
        await message.answer("Salom")
        
    else:
        await state.set_state(Register.fullname)

        await message.answer(
            text = check.return_message_text(1, user_lang)
        )
    
        print(database.return_users())
    
@router.message(Register.fullname)
async def get_fullname(message:Message, state:FSMContext):
    global user_lang
    fullname = message.text
    status = await check.check_fullname(fullname=fullname)
    
    if status:
        await state.update_data(fullname=fullname)
        await state.set_state(Register.year)
        await message.answer(
            text=check.return_message_text(3,user_lang)
        )
        
    else:
        await message.answer(
            text = check.return_message_text(2, user_lang)
        )
        
@router.message(Register.year)
async def get_year(message:Message, state:FSMContext):
    global user_lang
    year = message.text
    status = await check.check_year(year=year)
    
    if status:
        await state.update_data(year=year)
        await state.set_state(Register.address)
        await message.answer(
            text= check.return_message_text(5, user_lang)
        )
        
    else:
        await message.answer(
            text = check.return_message_text(4, user_lang)
        )
        
@router.message(Register.address)
async def get_address(message:Message, state:FSMContext):
    global user_lang
    address = message.text
    status = await check.check_address(address=address)

    if status:
        await state.update_data(address=address)
        await state.set_state(Register.email)
        await message.answer(
            text = check.return_message_text(c=7, lang=user_lang)
        )

    else: 
        
        await message.answer(
            text = check.return_message_text(6, user_lang)
        )
    
@router.message(Register.email)
async def get_email(message:Message, state:FSMContext):
    global user_lang
    email = message.text
    status = await check.check_email(email)
    
    if status:
        await state.update_data(email=email)
        await state.set_state(Register.password)
        await message.answer(
            text= check.return_message_text(c=9, lang=user_lang)
        )
    
    else:
        await message.answer(
            text=check.return_message_text(c=8, lang=user_lang)
        )
        

        
@router.message(Register.password)
async def get_password(message:Message, state:FSMContext):
    global user_lang
    password = message.text
    status = await check.check_password(password=password)
    
    phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=check.return_message_text(c=10, lang=user_lang), request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
    )
    
    if status:
        await state.update_data(password=password)
        global data
        data = await state.get_data()
        await state.clear()
        await message.answer(
            text=check.return_message_text(c=12, lang=user_lang),
            reply_markup=phone
        )
    
    else:
        await message.answer(
            text=check.return_message_text(c=11, lang=user_lang)
        )

@router.message(F.contact)
async def get_phone(message:Message, state:FSMContext):
    global user_lang
    
    phone = message.contact.phone_number
    
    data['phone_number'] = phone
    data['telegram_id'] = current_user.id
    
    status = check.check_is_registered(data)
    
    if status:
        await message.answer(
            text = check.return_message_text(13, user_lang)
        )
    else:
        await message.answer(
            text = check.return_message_text(14, user_lang)
        )




