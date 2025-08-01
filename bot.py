import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import notes
from keyboards.menu_kb import menu_keyboard

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(notes.router)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "<b>Привіт!</b> Я — твій Telegram-помічник ✨\n\n"
        "Вибери дію нижче 👇",
        reply_markup=menu_keyboard
    )


async def main():
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
