from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import home_keyboard
from src.db import chat_db


async def command_start(u: UpdateAdapter, bot: Bot):
    chat_db.upsert(u.chat_id)
    await bot.send_message(u.chat_id, "Hi, I'm a 'Study by sound Bot', send me a test, and I will sound it!",
                           reply_markup=home_keyboard)


async def processing(u: UpdateAdapter, bot: Bot):
    await bot.send_message(u.chat_id, "Please wait, processing your previous request...")


async def can_not_understand_you(u: UpdateAdapter, bot: Bot):
    await bot.send_message(u.chat_id, "Sorry, I can't understand you")
