#utils.py
import json
import logging
import os
from aiogram.fsm.state import StatesGroup, State

# Настройки логирования
logging.basicConfig(level=logging.INFO)

def load_quiz_data(QUIZ_DATA_PATH):
    if not os.path.exists(QUIZ_DATA_PATH):
        raise FileNotFoundError(f"Файл '{QUIZ_DATA_PATH}' не найден.")
    with open(QUIZ_DATA_PATH, encoding='utf-8') as file:
        return json.load(file)
    
class QuizGameState(StatesGroup):
    START_GAME = State()
    IN_PROGRESS = State()