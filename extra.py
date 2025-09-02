import requests
import json

# https://islomapi.uz/api/monthly?region=Toshkent&month=4

responce = requests.get("https://islomapi.uz/api/present/week?region=Toshkent")
print(json.dumps(responce.json(), indent = 4))


async def async_prayer_times_generator(data, lang="uz"):
    # Hafta/oy ma'lumotlari list bo'lishi mumkin
    if isinstance(data, dict):
        data_list = [data]
    else:
        data_list = data

    sticker = "🕌"
    weekdays_en = {
        "Dushanba": "Monday",
        "Seshanba": "Tuesday",
        "Chorshanba": "Wednesday",
        "Payshanba": "Thursday",
        "Juma": "Friday",
        "Shanba": "Saturday",
        "Yakshanba": "Sunday"
    }

    for day_data in data_list:
        date = day_data["date"].split(',')[0]
        hijri = f"{day_data['hijri_date']['month']}, {day_data['hijri_date']['day']}-kun"

        if lang == "uz":
            message = f"""
{sticker} <b>Hudud</b>: {day_data['region']}
<b>Sana</b>: {date}
<b>Hijriy sana</b>: {hijri}
<b>Hafta kuni</b>: {day_data['weekday']}

<b>Namoz vaqtlari</b>:  
<i>Tong saharlik</i>: {day_data['times']['tong_saharlik']}  
<i>Quyosh</i>: {day_data['times']['quyosh']}  
<i>Peshin</i>: {day_data['times']['peshin']}  
<i>Asr</i>: {day_data['times']['asr']}  
<i>Shom (iftor)</i>: {day_data['times']['shom_iftor']}  
<i>Hufton</i>: {day_data['times']['hufton']}  
"""
        else:
            hijri_en = f"{day_data['hijri_date']['month']}, {day_data['hijri_date']['day']}th day"
            message = f"""
{sticker} **Region:** {day_data['region']}
**Date:** {date}
**Hijri Date:** {hijri_en}
**Weekday:** {weekdays_en.get(day_data['weekday'], day_data['weekday'])}

**Prayer Times:**  
- Fajr: {day_data['times']['tong_saharlik']}  
- Sunrise: {day_data['times']['quyosh']}  
- Dhuhr: {day_data['times']['peshin']}  
- Asr: {day_data['times']['asr']}  
- Maghrib (Iftar): {day_data['times']['shom_iftor']}  
- Isha: {day_data['times']['hufton']}  
"""

        yield message.strip()
