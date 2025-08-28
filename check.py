import asyncio
from datetime import datetime as dt

async def check_fullname(fullname: str):
    
    for i in fullname.lower():
        if not (i.isalpha() or i in ["'", "’", " "]):
            return False
    
    return False if len(fullname.split()) != 4 or not (fullname.endswith("qizi") or fullname.endswith("o'g'li") or fullname.endswith("o’g’li"))  else  True
        
async def check_year(year:str):
    year = int(year)
    return True if year<1970 and year>dt.now().year else True
        
        