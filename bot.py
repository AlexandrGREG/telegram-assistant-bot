# bot.py
import threading
import asyncio
from telegram_bot_main import run_bot
from web_stub import app


def start_web():
    app.run(host="0.0.0.0", port=10000)


if __name__ == "__main__":
    # Запускаємо веб-сервер у окремому потоці
    threading.Thread(target=start_web).start()

    # Запускаємо Telegram-бота
    asyncio.run(run_bot())
