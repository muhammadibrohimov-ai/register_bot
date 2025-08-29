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

user_lang = "uz"

@router.message(CommandStart())
async def cmd_start(message: Message, state:FSMContext):
    global current_user
    current_user = message.from_user
    await state.set_state(Register.fullname)
    await message.answer(
        text="Namoz vaqtlari botga xush kelibsiz!\nWelcome to the prayer times bot\n\nTilni kiritng:\nChoose the language: ",
        reply_markup=start_keyboards
    )


@router.message(F.text=='uz')
async def register_uz(message:Message, state:FSMContext):
    if not message.text == "uz":
        user_lang = "en"

    await state.set_state(Register.fullname)

    await message.answer(
        text = check.return_message_text(1, user_lang)
    )
    
@router.message(Register.fullname)
async def get_fullname(message:Message, state:FSMContext):
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
    address = message.text
    status = await check.check_address(address=address)

    if status:
        await state.update_data(address=address)
        await state.set_state(Register.email)
        await message.answer(
            text = "Emailnigizni kiriting: "
        )

    else: 
        
        await message.answer(
            text = check.return_message_text(6, user_lang)
        )
    
@router.message(Register.email)
async def get_email(message:Message, state:FSMContext):
    email = message.text
    status = await check.check_email(email)
    
    if status:
        await state.update_data(email=email)
        await state.set_state(Register.password)
        await message.answer(
            text='Parol yarating: '
        )
    
    else:
        await message.answer(
            text="Email to'g'ri formatda emas, yoki allaqachon foydalanilgan, qayta urining!"
        )
        
phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Jo'natish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
        
@router.message(Register.password)
async def get_password(message:Message, state:FSMContext):
    password = message.text
    status = await check.check_password(password=password)
    
    if status:
        await state.update_data(password=password)
        global data
        data = await state.get_data()
        await state.clear()
        await message.answer(
            text="Telefon raqamingizni jo'nating",
            reply_markup=phone
        )
    
    else:
        await message.answer(
            text="Parolingiz bizning talabimizga mos kelmadi, qayta urining!"
        )

@router.message(F.contact)
async def get_phone(message:Message, state:FSMContext):
    phone = message.contact.phone_number
    data['phone_number'] = phone
    await message.answer(
        text=f'Ro\'yxatdan muvaffaqiyatli o\'tdingiz {data}'
    )


async def get_users():
    query = "SELECT * FROM users;"
    data = await database.get_data(query)

    if not data or data == []:
        await database.create_table_users()
        data = []

    return data