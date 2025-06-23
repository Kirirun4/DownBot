# keyboards.py
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

def start_game_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Викторина"), KeyboardButton(text="Статистика"))
    return builder.as_markup(resize_keyboard=True)

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(answer_options):
        if option == right_answer:
            builder.button(text=option, callback_data=f"right_answer_{i}")
        else:
            builder.button(text=option, callback_data=f"wrong_answer_{i}")
    builder.adjust(1)
    return builder.as_markup()