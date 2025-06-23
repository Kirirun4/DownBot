# database.py
import aiosqlite
from config import DB_NAME

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER
            );
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                correct_answers INTEGER DEFAULT 0,
                incorrect_answers INTEGER DEFAULT 0
            );
        ''')
        await db.commit()

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0
        
async def save_result(user_id, is_correct):
    async with aiosqlite.connect(DB_NAME) as db:
        column_to_update = "correct_answers" if is_correct else "incorrect_answers"
        await db.execute(f'''
            INSERT INTO quiz_results (user_id, {column_to_update}) 
            VALUES (:user_id, :value)
            ON CONFLICT(user_id) DO UPDATE SET {column_to_update}=quiz_results.{column_to_update}+1''',
                        {"user_id": user_id, "value": 1})
        await db.commit()

async def get_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_results WHERE user_id=?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return {
                "correct_answers": row[1],
                "incorrect_answers": row[2]
            } if row else None