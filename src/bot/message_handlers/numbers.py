from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.db import chat_db
from src.db import infinity_numbers_db
from src.db.chat_db import ChatStatus
from src.db.infinity_numbers_db import InfinityNumbers


async def command_numbers_study(u: UpdateAdapter, bot: Bot):
    chat_db.update_status(u.chat_id, ChatStatus.NUMBERS_STUDY)
    split = u.text.split()
    if len(split) == 2:
        range_from = 0
        range_to = 0
    elif len(split) == 3:
        range_from = split[1]
        range_to = split[2]
    else:
        raise ValueError("to do error")
    infinity_numbers_db.upsert(InfinityNumbers(u.chat_id, range_from, range_to))
    await bot.send_message(u.chat_id, "You start command_numbers_study")


async def command_numbers_test(u: UpdateAdapter, bot: Bot):
    chat_db.update_status(u.chat_id, ChatStatus.NUMBERS_TEST)
    await bot.send_message(u.chat_id, "You start command_numbers_test")


async def numbers_study_progress(u: UpdateAdapter, bot: Bot):
    await bot.send_message(u.chat_id, "numbers_study_progress")


async def numbers_test_progress(u: UpdateAdapter, bot: Bot):
    await bot.send_message(u.chat_id, "numbers_test_progress")
