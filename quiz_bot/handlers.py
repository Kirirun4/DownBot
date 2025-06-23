# handlers.py
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards import *
from database import *
from utils import *
from config import QUIZ_DATA_PATH

quiz_data = load_quiz_data(QUIZ_DATA_PATH)

async def start_handler(message: Message, state: FSMContext):
    await state.set_state(QuizGameState.START_GAME)
    await message.answer("Добро пожаловать в квиз! Нажмите 'Викторина'.", reply_markup=start_game_kb())

async def quiz_handler(message: Message, state: FSMContext):
    await state.set_state(QuizGameState.IN_PROGRESS)
    await message.answer("Начинаем квиз!")
    await new_quiz(message)

async def new_quiz(message: Message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

async def get_question(message: Message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    options = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(options, options[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def right_answer(callback: CallbackQuery, state: FSMContext):
    selected_answer = callback.data.split("_")[1]
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None)
    await callback.message.answer(f"Ваш выбор: {selected_answer}\nПравильно!")
    await save_result(callback.from_user.id, True)
    await next_question(callback)

async def wrong_answer(callback: CallbackQuery, state: FSMContext):
    selected_answer = callback.data.split("_")[1]
    await callback.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id, reply_markup=None)
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]["correct_option"]
    await callback.message.answer(f"Ваш выбор: {selected_answer}\nНеверно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    await save_result(callback.from_user.id, False)
    await next_question(callback)

async def next_question(callback: CallbackQuery):
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Квиз завершён. Для перезапуска викторины введите: /start")

async def stats_handler(message: Message):
    user_id = message.from_user.id
    stats = await get_stats(user_id)
    if stats:
        await message.answer(f"Твоя статистика:\nПравильных ответов: {stats['correct_answers']}\nОшибочных ответов: {stats['incorrect_answers']}")
    else:
        await message.answer("Вы ещё не играли ни одного квиза.")