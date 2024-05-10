from datetime import datetime
import random
import string


async def get_date():
    dateTimeObj = f"{datetime.utcnow()}"
    date_time_obj = datetime.strptime(dateTimeObj, "%Y-%m-%d %H:%M:%S.%f")
    date: str = f"{date_time_obj.strftime('%Y-%m-%d')}"

    return date


async def generate_random_code(length):
    code = ''.join(random.choices(string.digits[1:], k=length))
    return code
