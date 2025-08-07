# telegram_bot_main.py
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import asyncio

from handlers import notes  # твій маршрутизатор

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(notes.router)


async def run_bot():
    await dp.start_polling(bot)
