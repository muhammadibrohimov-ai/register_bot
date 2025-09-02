import requests

import aiohttp
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from .handlers_uz import *

from .buttons import *
from outer import check

import extra

router = Router()

from .buttons import *

@router.message(F.text.in_(time_en+time_uz))
async def regions(message:Message):
    
    global c
    
    if message.text in ['Oylik', "Monthly"]:
        c = 3
    elif message.text in ['Haftalik', 'Weekly']:
        c = 2
    else:
        c=1
    
    global user_lang
    user_lang = get_lang()
    
    await message.answer(
        text = check.return_message_text(16, user_lang),
        reply_markup=await return_regions(user_lang)
    )



    
@router.callback_query(F.data.in_(viloyatlar))
async def get_prayer_times(callback:CallbackQuery):
    region = callback.data
    callback.answer(region)

    print(region)


    if region == "Farg'ona":
        region = 'Farg\'ona'

    match c:
        case 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://islomapi.uz/api/present/day?region={region}") as resp:
                    data = await resp.json()

            async for message in extra.async_prayer_times_generator(data,user_lang):
                await callback.message.answer(
                    text = message
                )
            
        case 2:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://islomapi.uz/api/present/week?region={region}") as resp:
                    data = await resp.json()

            async for message in extra.async_prayer_times_generator(data,user_lang):
                await callback.message.answer(
                    text = message
                )
                
                
        case 3:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://islomapi.uz/api/monthly?region={region}&month={datetime.now().month}") as resp:
                    data = await resp.json()

            async for message in extra.async_prayer_times_generator(data,user_lang):
                await callback.message.answer(
                    text = message
                )


@router.message()
async def nothing(message:Message):
    await message.answer(
        text = "Iltimos /help komandasini yuboring!"
    )