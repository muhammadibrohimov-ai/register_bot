# Additional modules

import asyncio
import logging
import database
import check

# Main module

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Token and Dispatcher

from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher()

# Keyboards

start_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="uz"), KeyboardButton(text='en')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Jo'natish", request_contact=True)]
    ],
    resize_keyboard=True
)

# Finite State Machine subclass

class Register(StatesGroup):
    fullname = State()
    year = State()
    address = State()
    email = State()
    password = State()

@dp.message(CommandStart())
async def cmd_start(message: Message, state:FSMContext):
    global current_user
    current_user = message.from_user
    state.set_state(Register.fullname)
    await message.answer(
        text="Register botga xush kelibsiz!\n\nTilni kiritng:",
        reply_markup=start_keyboards
    )


@dp.message(F.text=='uz')
async def register_uz(message:Message, state:FSMContext):
    await state.set_state(Register.fullname)
    await message.answer("To'liq isminginzi kiritng (Ali Aliyev Alijon o'g'li (qizi)): ")
    
@dp.message(Register.fullname)
async def get_fullname(message:Message, state:FSMContext):
    fullname = message.text
    status = await check.check_fullname(fullname=fullname)
    if status:
        await state.update_data(fullname=fullname)
        await state.set_state(Register.year)
        await message.answer(
            text="Tug'ilgan yilingizni kiritng: ",
        )
    else:
        await message.answer("Ismingiz not'og'ri formatda kiritlgan ekan qayta uruning (Ali Aliyev Alijon o'g'li (qizi)): ")


async def get_users():
    query = "SELECT * FROM users;"
    data = database.get_data(query)

    if not data or data == []:
        database.create_table_users()
        data = []

    return data

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except:
        print("EXIT")