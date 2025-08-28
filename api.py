import requests
import json
from datetime import datetime as dt, timedelta


def get_times(c, city="Fergana", date=dt.now()):
    match c:

        case 1:  
            
            # Oylik
            # Aladhan API faqat kunlik, shuning uchun oyning barcha kunlarini olish uchun sikl qilish kerak
            
            results = []
            
            for i in range(1, 32):
            
                try:
                    url = "http://api.aladhan.com/v1/timingsByCity"
                    response = requests.get(url, params={
                        "city": city,
                        "country": "Uzbekistan",
                        "method": 2,
                        "date": (dt.now() + timedelta(days=i)).strftime("%d-%m-%Y")
                    }).json()
                    results.append({f"{day}-{date.month}-{date.year}": response['data']['timings']})
            
                except:
                    continue
            
            return results

        case 2:  # Haftalik
            results = []
            start_day = date
            for i in range(7):
                day = start_day + timedelta(days=i)
                try:
                    url = "http://api.aladhan.com/v1/timingsByCity"
                    response = requests.get(url, params={
                        "city": "Fergana",
                        "country": "Uzbekistan",
                        "method": 2,
                        "date": day.strftime("%d-%m-%Y")
                    }).json()
                    results.append({day.strftime("%d-%m-%Y"): response['data']['timings']})
                except:
                    continue
            return results

        case 3:  # Bugungi kun
            url = "http://api.aladhan.com/v1/timingsByCity"
            response = requests.get(url, params={
                "city": "Fergana",
                "country": "Uzbekistan",
                "method": 2,
                "date": date.strftime("%d-%m-%Y")
            }).json()
            return response['data']['timings']

        case 4:  # Ma'lum sana
            try:
                date_obj = dt.strptime(date, "%d-%m-%Y")
                url = "http://api.aladhan.com/v1/timingsByCity"
                response = requests.get(url, params={
                    "city": "Fergana",
                    "country": "Uzbekistan",
                    "method": 2,
                    "date": date_obj.strftime("%d-%m-%Y")
                }).json()
                return response['data']['timings']
            except:
                return "Kun xato formatda kiritlgan! (kun-oy-yil formatida kiritng)"
