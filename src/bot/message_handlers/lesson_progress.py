from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.db import chat_db, lesson_progress_db
from src.db.chat_db import ChatStatus
from src.service.audio_files import sound_audio


async def start_lesson(u: UpdateAdapter, bot: Bot, group_title: str):
    await bot.edit_message_text(f"You start lesson *{group_title}*",
                                u.chat_id,
                                u.original_message_id,
                                parse_mode="markdown")
    chat_db.update_status(u.chat_id, ChatStatus.STUDYING_LESSON)
    lesson_progress_db.new_attempt(u.chat_id, group_title)
    # todo to pass this exam you have to pass x words with more then y success score
    # todo close last lesson_progress on exit
    # todo clear attempt on start command
    await send_random_audio_from_lesson(u, bot)


async def send_random_audio_from_lesson(u: UpdateAdapter, bot: Bot):
    word = lesson_progress_db.new_random_word(u.chat_id)
    language = chat_db.find_by_id(u.chat_id).language_code
    await bot.send_audio(u.chat_id, sound_audio(language, word, "test"))


async def lesson_progress(u: UpdateAdapter, bot: Bot):
    is_correct, original_value = lesson_progress_db.save_chat_answer(u.chat_id, u.text)
    if is_correct:
        await bot.send_message(u.chat_id, "Correct")
    else:
        await bot.send_message(u.chat_id, f"Incorrect, it was _{original_value}_", "markdown")
    # seave chat answer
    # calculate score
    correct_count, all_count = lesson_progress_db.get_score(u.chat_id)
    await bot.send_message(u.chat_id, f"Your progress is {correct_count}/{all_count}")
    await send_random_audio_from_lesson(u, bot)
