from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import home_keyboard
from src.db import chat_db, lesson_progress_db
from src.db.chat_db import ChatStatus
from src.service.audio_files import sound_audio
from src.service.translate import translate

CALLBACK_PREFIX: str = "LESSON_"
REQUIRED_WORDS: int = 15
REQUIRED_RATE: float = 0.8


def reply_markup(correct_count: int, all_count: int):
    if all_count >= REQUIRED_WORDS and correct_count / all_count >= REQUIRED_RATE:
        return ReplyKeyboardMarkup([[KeyboardButton("✅")]])
    else:
        return ReplyKeyboardMarkup([[KeyboardButton("❌")]])


async def start_lesson(u: UpdateAdapter, bot: Bot, group_title: str):
    await bot.edit_message_text(
        f"You start lesson *{group_title}*",
        u.chat_id,
        u.original_message_id,
        parse_mode="markdown")
    await bot.send_message(
        u.chat_id,
        f"To pass this lesson you have pass at list {REQUIRED_WORDS} words with min score rate {REQUIRED_RATE * 100}%",
        reply_markup=reply_markup(0, 0))
    chat_db.update_status(u.chat_id, ChatStatus.STUDYING_LESSON)
    lesson_progress_db.new_attempt(u.chat_id, group_title)
    await send_random_audio_from_lesson(u, bot)


async def send_random_audio_from_lesson(u: UpdateAdapter, bot: Bot):
    word = lesson_progress_db.select_random_word(u.chat_id)
    chat = chat_db.find_by_id(u.chat_id)
    if chat.language.code != "en-US":
        word = translate(chat.language.translate_api_code, word)
    lesson_progress_db.save_word(u.chat_id, word)
    audio = sound_audio(chat.language.code, word, "test")
    await bot.send_audio(u.chat_id, audio)


async def lesson_progress(u: UpdateAdapter, bot: Bot):
    if u.text == "✅" or u.text == "❌":
        lesson_progress_db.delete_last_word(u.chat_id)
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
        correct_count, all_count = lesson_progress_db.get_score(u.chat_id)
        score = f"\nYour score is {correct_count}/{all_count}"
        if u.text == "✅":
            await bot.send_message(u.chat_id, f"You have passed this lesson ✅{score}", reply_markup=home_keyboard)
        else:
            await bot.send_message(u.chat_id, f"You have canceled this lesson ❌{score}", reply_markup=home_keyboard)
        return
    is_correct, original_value = lesson_progress_db.save_chat_answer(u.chat_id, u.text)
    correct_count, all_count = lesson_progress_db.get_score(u.chat_id)
    score_info = f"Your progress is {correct_count}/{all_count}"
    markup = reply_markup(correct_count, all_count)
    if is_correct:
        await bot.send_message(u.chat_id, f"Correct\n{score_info}", reply_markup=markup)
    else:
        await bot.send_message(u.chat_id,
                               f"Incorrect, it was _{original_value}_\n{score_info}",
                               "markdown",
                               reply_markup=markup)
    await send_random_audio_from_lesson(u, bot)
