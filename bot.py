# Additional modules

import asyncio
import logging

# Main module

from aiogram import Bot, Dispatcher
import handlers_uz

# Token and Dispatcher

from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN)
    dp.include_router(handlers_uz.router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except:
        print("EXIT")