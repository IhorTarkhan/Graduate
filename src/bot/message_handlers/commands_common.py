from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import home_keyboard
from src.db import chat_db
from src.db import lesson_progress_db


async def command_start(u: UpdateAdapter, bot: Bot):
    chat_db.upsert(u.chat_id)
    lesson_progress_db.delete_chat_data(u.chat_id)
    await bot.send_message(u.chat_id,
                           "Hi, I'm a `Study by sound Bot`, send me a test, and I will sound it!",
                           parse_mode="markdown",
                           reply_markup=home_keyboard)


async def command_help(u: UpdateAdapter, bot: Bot):
    await bot.send_message(u.chat_id, "In dev")
