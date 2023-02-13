from typing import Optional

from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import home_keyboard, BotCommand
from src.db import chat_db
from src.db import infinity_numbers_db
from src.db.chat_db import ChatStatus
from src.db.infinity_numbers_db import InfinityNumbers
from src.service.audio_files import sound_audio


async def command_numbers_study(u: UpdateAdapter, bot: Bot):
    chat_db.update_status(u.chat_id, ChatStatus.NUMBERS_STUDY)
    save_range(u, "Incorrect format:\n" + BotCommand.NUMBERS_STUDY.help())
    await bot.send_message(u.chat_id,
                           "You start *Numbers study*",
                           parse_mode="markdown",
                           reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Exit 🚪")], [KeyboardButton("Next ⏭️")]]))
    await generate_and_send_new_number(u, bot)


async def numbers_study_progress(u: UpdateAdapter, bot: Bot):
    if u.text == "Exit 🚪":
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
        await bot.send_message(u.chat_id, "You have exit 🚪", reply_markup=home_keyboard)
    else:
        await generate_and_send_new_number(u, bot)


async def command_numbers_test(u: UpdateAdapter, bot: Bot):
    chat_db.update_status(u.chat_id, ChatStatus.NUMBERS_TEST)
    save_range(u, "Incorrect format:\n" + BotCommand.NUMBERS_TEST.help())
    await bot.send_message(u.chat_id,
                           "You start *Numbers test*",
                           parse_mode="markdown",
                           reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Exit 🚪")]]))
    await generate_and_send_new_number(u, bot, "test")


async def numbers_test_progress(u: UpdateAdapter, bot: Bot):
    if u.text == "Exit 🚪":
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
        await bot.send_message(u.chat_id, "You have exit 🚪", reply_markup=home_keyboard)
        return
    ln = infinity_numbers_db.get_last_number_to(u.chat_id)
    try:
        int(u.text)
    except ValueError:
        raise ValueError(f"Can not parse `{u.text}` as integer, you have enter numbers only")
    if ln == int(u.text):
        await bot.send_message(u.chat_id, "Correct)")
    else:
        await bot.send_message(u.chat_id, f"Incorrect(\nIt was {ln}")
    await generate_and_send_new_number(u, bot, "test")


def save_range(u: UpdateAdapter, error_message: str):
    split = u.text.split()
    if len(split) == 2:
        val = int(split[1])
        if val > 0:
            range_from = 0
            range_to = val
        else:
            range_from = val
            range_to = 0
    elif len(split) == 3:
        val_from = int(split[1])
        val_to = int(split[2])
        if val_from >= val_to:
            val_from, val_to = val_to, val_from
        range_from = val_from
        range_to = val_to
    else:
        raise ValueError(error_message)
    infinity_numbers_db.upsert(InfinityNumbers(u.chat_id, range_from, range_to))


async def generate_and_send_new_number(u: UpdateAdapter, bot: Bot, title: Optional[str] = None):
    infinity_numbers_db.update_last_number_to(u.chat_id)
    ln = infinity_numbers_db.get_last_number_to(u.chat_id)
    language = chat_db.find_by_id(u.chat_id).language.code
    audio_link = sound_audio(language, str(ln), title)
    await bot.send_audio(u.chat_id, audio_link)
