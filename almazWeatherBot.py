import requests
import datetime
from config import bot_token, open_weather_key
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello! Enter a city and I will show it's weather!")

@dp.message_handler()
async def get_weather(message: types.Message):
    codeIconConvert = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_key}&units=metric")
        data = r.json()

        city = data["name"]
        temperature = data["main"]["temp"]
        description = data["weather"][0]["main"]
        if description in codeIconConvert:
            desc = codeIconConvert[description]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        clouds = data["clouds"]["all"]
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"\nПогода в городе {city}: {desc}\nТемпература: {temperature}°C 🌡️"    
        f"\nВлажность: {humidity}% \U0001F4A6\n"
        f"Скорость ветра: {wind_speed} м/с  \U0001F4A8\nОблачность: {clouds}% \U00002601")
    except:
        await message.reply("Check the city name")    


if __name__ == '__main__':
    executor.start_polling(dp)