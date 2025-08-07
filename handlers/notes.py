from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import json
import os
from aiogram.fsm.context import FSMContext
from states import NoteFSM
from keyboards.menu_kb import menu_keyboard

router = Router()
NOTES_FILE = "notes.json"


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def build_keyboard(note_titles):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"📝 {title}", callback_data=f"show_note|{title}"),
            InlineKeyboardButton(
                text="🗑 Видалити", callback_data=f"delete_note|{title}")
        ]
        for title in note_titles
    ])


@router.message(F.text == "🚀 Старт")
async def start_handler(message: types.Message):
    await message.answer(
        "<b>Привіт!</b> Я — твій Telegram-помічник ✨\n\n"
        "Вибери дію нижче 👇",
        reply_markup=menu_keyboard,
        parse_mode="HTML"
    )


@router.message(F.text == "📝 Додати нотатку")
async def add_note_start(message: types.Message, state: FSMContext):
    await state.set_state(NoteFSM.waiting_for_title)
    await message.answer("📝 Введи назву нотатки:")


@router.message(NoteFSM.waiting_for_title)
async def add_note_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(NoteFSM.waiting_for_content)
    await message.answer("✏️ Тепер введи зміст нотатки:")


@router.message(NoteFSM.waiting_for_content)
async def add_note_content(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    title = user_data['title']
    content = message.text
    user_id = str(message.from_user.id)

    notes = load_notes()
    if user_id not in notes:
        notes[user_id] = {}
    notes[user_id][title] = content
    save_notes(notes)

    await state.clear()
    await message.answer("✅ Нотатку збережено!", reply_markup=menu_keyboard)


@router.message(F.text == "📋 Мої нотатки")
async def cmd_shownotes(message: Message):
    user_id = str(message.from_user.id)
    notes = load_notes()
    user_notes = notes.get(user_id)

    if not user_notes:
        await message.answer("😔 У тебе поки немає нотаток.")
        return

    kb = build_keyboard(user_notes.keys())
    await message.answer("Ось твої нотатки:", reply_markup=kb)


@router.callback_query(F.data.startswith("show_note|"))
async def show_note_content(callback: CallbackQuery):
    title = callback.data.split("|")[1]
    user_id = str(callback.from_user.id)
    notes = load_notes()
    user_notes = notes.get(user_id, {})
    note_text = user_notes.get(title, "")
    await callback.message.answer(
        f"📌<b>{title}</b>\n{note_text if note_text else 'Порожня нотатка.'}",
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("delete_note|"))
async def delete_note(callback: CallbackQuery):
    title = callback.data.split("|")[1]
    user_id = str(callback.from_user.id)
    notes = load_notes()
    user_notes = notes.get(user_id, {})
    if title in user_notes:
        del user_notes[title]
        notes[user_id] = user_notes
        save_notes(notes)
        await callback.message.answer(f"❌ Нотатку <b>{title}</b> видалено.", reply_markup=menu_keyboard)
    else:
        await callback.message.answer("Нотатку не знайдено.", reply_markup=menu_keyboard)
    await callback.answer()
