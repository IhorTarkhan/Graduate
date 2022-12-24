from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.db import chat_db, lesson_attempt_db, lesson_progress_db, basic_words_db
from src.db.lesson_progress_db import LessonProgress
from src.service.audio_files import sound_audio


async def start_lesson(u: UpdateAdapter, bot: Bot, group_title: str):
    lesson_attempt_db.new_attempt(u.chat_id, group_title)
    # todo to pass this exam you have to pass x words with more then y success score
    # todo close last lesson_progress on exit
    await send_random_audio_from_lesson(u, bot)


async def send_random_audio_from_lesson(u: UpdateAdapter, bot: Bot):
    attempt = lesson_attempt_db.get_active_attempt(u.chat_id)
    language = chat_db.find_by_id(u.chat_id).language_code
    word = basic_words_db.select_random_word(attempt.group_name)
    lesson_progress_db.insert_new(attempt.id, word)
    await bot.send_audio(u.chat_id, sound_audio(language, word, "test"))


async def lesson_progress(u: UpdateAdapter, bot: Bot):
    progress: LessonProgress = lesson_progress_db.get_active(u.chat_id)
    if u.text.lower() == progress.word.lower():
        await bot.send_message(u.chat_id, "Correct")
    else:
        await bot.send_message(u.chat_id, f"Incorrect, it was _{progress.word}_", "markdown")
    lesson_progress_db.set_chat_answer(progress.id, u.text)
    attempt = lesson_attempt_db.get_active_attempt(u.chat_id)
    await bot.send_message(u.chat_id, f"Your progress is {attempt.correct_word_count}/{attempt.word_count}")
    await send_random_audio_from_lesson(u, bot)
