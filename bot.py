import asyncio
import logging
import database
import check

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



from environs import Env

class Register(StatesGroup):
    fullname = State()
    year = State()
    address = State()
    email = State()
    password = State()

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher()

status = True

start_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="uz"), KeyboardButton(text='en')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message(CommandStart())
async def cmd_start(message: Message, state=FSMContext):
    current_user = message.from_user
    state.set_state(Register.fullname)
    await message.answer(
        text="Register botga xush kelibsiz!\n\nTilni kiritng:",
        reply_markup=start_keyboards
    )

@dp.message(Register.name)
@dp.message(F.text=='uz')
async def register_uz(message:Message, state=FSMContext):
    
@dp.message(Register.year)
async def get

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