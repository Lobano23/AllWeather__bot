import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')
OPENWEATHERMAP_API_KEY=os.getenv('OPENWEATHERMAP_API_KEY')

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply('Напиши название города и я передам прогноз погоды')
@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        city_name = message.text
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&lang=ru&appid={OPENWEATHERMAP_API_KEY}")
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        await message.reply(f"Погода в городе {city}:\nТекущая температура: {cur_temp}°C\nВлажность: {humidity}%\nДавление: {pressure} мм рт. ст.\nСкорость ветра: {wind} м/с")
    except:
        await message.reply('Проверьте название города')

if __name__ == "__main__":
    executor.start_polling(dp)