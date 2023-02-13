from typing import Optional

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
at_less_info_required: str = f"{int(REQUIRED_RATE * REQUIRED_WORDS)}/{REQUIRED_WORDS} required"


async def start_lesson(u: UpdateAdapter, bot: Bot, group_title: str):
    await bot.edit_message_text(
        f"You start lesson *{group_title}*",
        u.chat_id,
        u.original_message_id,
        parse_mode="markdown")
    await bot.send_message(
        u.chat_id,
        f"To pass this lesson {at_less_info_required}",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🚪")]]))
    chat_db.update_status(u.chat_id, ChatStatus.STUDYING_LESSON)
    lesson_progress_db.new_attempt(u.chat_id, group_title)
    await send_random_audio_from_lesson(u, bot)


async def send_random_audio_from_lesson(u: UpdateAdapter, bot: Bot):
    word, group = lesson_progress_db.select_random_word(u.chat_id)
    chat = chat_db.find_by_id(u.chat_id)
    if chat.language.code != "en-US":
        word = translate(chat.language.translate_api_code, word)
    lesson_progress_db.save_word(u.chat_id, word)
    audio = sound_audio(chat.language.code, word, f"{group}-{chat.language.name}")
    await bot.send_audio(u.chat_id, audio)


def format_current_score(correct_count: int, all_count: int, required_count: Optional[bool] = False) -> str:
    if required_count and REQUIRED_WORDS > all_count:
        return f"Your score is {correct_count}/{all_count} ({REQUIRED_WORDS - all_count} left, {at_less_info_required})"
    else:
        return f"Your score is {correct_count}/{all_count} ({at_less_info_required})"


async def lesson_progress(u: UpdateAdapter, bot: Bot):
    if u.text == "🚪":
        lesson_progress_db.delete_last_word(u.chat_id)
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
        correct_count, all_count = lesson_progress_db.get_score(u.chat_id)
        await bot.send_message(u.chat_id,
                               f"You have canceled this lesson 🚪\n" + format_current_score(correct_count, all_count),
                               reply_markup=home_keyboard)
        return
    is_correct, original_value = lesson_progress_db.save_chat_answer(u.chat_id, u.text)
    correct_count, all_count = lesson_progress_db.get_score(u.chat_id)
    score_info = format_current_score(correct_count, all_count, True)
    if is_correct:
        is_correct_msg = f"Correct"
    else:
        is_correct_msg = f"Incorrect, it was _{original_value}_"
    if correct_count >= int(REQUIRED_RATE * REQUIRED_WORDS):
        result = "Congrats ✅"
    else:
        result = "Unfortunately you failed ❌"
    if all_count == REQUIRED_WORDS:
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
        await bot.send_message(u.chat_id,
                               f"{is_correct_msg}\n{score_info}\n\n{result}",
                               "markdown",
                               reply_markup=home_keyboard)
    else:
        await bot.send_message(u.chat_id, f"{is_correct_msg}\n{score_info}", "markdown")
        await send_random_audio_from_lesson(u, bot)
