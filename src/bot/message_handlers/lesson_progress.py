from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.db import chat_db, lesson_attempt_db, lesson_progress_db, basic_words_db
from src.db.lesson_progress_db import LessonProgress
from src.service.audio_files import sound_audio


async def start_lesson(chat_id: int, group_title: str, bot: Bot):
    lesson_attempt_db.insert_new(chat_id, group_title)
    active_attempt = lesson_attempt_db.get_active(chat_id)
    language = chat_db.find_by_id(chat_id).language_code
    word = basic_words_db.select_random_word(group_title)
    lesson_progress_db.insert_new(active_attempt.id, word)
    await bot.send_audio(chat_id, sound_audio(language, word, "test"))


async def lesson_progress(u: UpdateAdapter, bot: Bot):
    progress: LessonProgress = lesson_progress_db.get_active(u.chat_id)
    if u.text.lower() == progress.word.lower():
        await bot.send_message(u.chat_id, "Correct")
    else:
        await bot.send_message(u.chat_id, f"Incorrect, it was {progress.word}")
    lesson_progress_db.set_chat_answer(progress.id, u.text)
    attempt = lesson_attempt_db.get_active(u.chat_id)
    await bot.send_message(u.chat_id, f"Your progress is {attempt.correct_word_count}/{attempt.word_count}")
    language = chat_db.find_by_id(u.chat_id).language_code
    word = basic_words_db.select_random_word(attempt.group_name)
    lesson_progress_db.insert_new(attempt.id, word)
    await bot.send_audio(u.chat_id, sound_audio(language, word, "test"))
