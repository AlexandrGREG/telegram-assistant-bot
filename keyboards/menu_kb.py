from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Старт")],
        [KeyboardButton(text="📝 Додати нотатку")],
        [KeyboardButton(text="📋 Мої нотатки")]
    ],
    resize_keyboard=True
)
