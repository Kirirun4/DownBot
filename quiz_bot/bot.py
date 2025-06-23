# bot.py
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import Command
from config import API_TOKEN
from handlers import *
from utils import QuizGameState
from database import create_table
import asyncio

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Подключаем обработчики
router.message.register(start_handler, Command("start"))
router.message.register(quiz_handler, F.text == "Викторина", QuizGameState.START_GAME)
router.message.register(stats_handler, Command("stats"))
router.message.register(stats_handler, F.text == "Статистика")
router.callback_query.register(right_answer, F.data.startswith("right_answer_"), QuizGameState.IN_PROGRESS)
router.callback_query.register(wrong_answer, F.data.startswith("wrong_answer_"), QuizGameState.IN_PROGRESS)

dp.include_router(router)

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())