# states.py
from aiogram.fsm.state import State, StatesGroup


class NoteFSM(StatesGroup):
    waiting_for_title = State()
    waiting_for_content = State()
