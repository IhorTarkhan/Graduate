from telegram import Update
from telegram.ext import CallbackContext

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import BotCommand, BotKeyboardButton
from src.bot.message_handlers.change_voice_language import \
    change_voice_language, \
    start_change_voice_language_flow, \
    callback_prefix as change_voice_language_prefix
from src.bot.message_handlers.common import command_start, processing
from src.bot.message_handlers.lesson_progress import lesson_progress
from src.bot.message_handlers.select_leson import \
    start_select_lesson_flow, \
    select_lesson, \
    callback_prefix as select_lesson_prefix
from src.bot.message_handlers.sound_text import sound_text
from src.db import chat_db
from src.db.chat_db import ChatStatus


async def handle_message(update: Update, context: CallbackContext):
    u = UpdateAdapter(update)
    bot = context.bot

    chat_db.insert_if_not_exist(u.chat_id)
    status: ChatStatus = chat_db.find_by_id(u.chat_id).status
    if u.is_text(BotCommand.COMMAND_START):
        await command_start(u, bot)
    elif status == ChatStatus.PROCESSING:
        await processing(u, bot)
    elif status == ChatStatus.STUDYING_LESSON:
        await lesson_progress(u, bot)
    elif u.is_command_start_with(change_voice_language_prefix):
        await change_voice_language(u, bot)
    elif u.is_command_start_with(select_lesson_prefix):
        await select_lesson(u, bot)
    elif u.is_text(BotKeyboardButton.TAKE_A_LESSON):
        await start_select_lesson_flow(u, bot)
    elif u.is_text(BotKeyboardButton.CHANGE_VOICE_LANGUAGE):
        await start_change_voice_language_flow(u, bot)
    else:
        await sound_text(u, bot)
