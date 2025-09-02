import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import additional

from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
dp = Dispatcher(storage=MemoryStorage())


async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp.include_router(additional.handlers_uz.router)
    dp.include_router(additional.times_handlers.router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Bot stopped")
