import logging
from typing import Union, Any

from telegram import Update
from telegram.ext import CallbackContext

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import BotCommand, BotKeyboardButton
from src.bot.message_handlers.change_voice_language import change_voice_language, start_change_voice_language_flow
from src.bot.message_handlers.commands import command_start, processing, command_help, command_numbers_study, \
    command_numbers_test
from src.bot.message_handlers.lesson_progress import lesson_progress
from src.bot.message_handlers.select_leson import start_select_lesson_flow, select_lesson
from src.bot.message_handlers.sound_text import sound_text
from src.db import chat_db
from src.db.Transaction import Transaction
from src.db.chat_db import ChatStatus


async def handle_text(update: Update, context: CallbackContext):
    Transaction.open()
    u = UpdateAdapter(update)
    bot = context.bot

    chat_db.insert_if_not_exist(u.chat_id)
    status: ChatStatus = chat_db.find_by_id(u.chat_id).status
    if u.is_text(BotCommand.START):
        await command_start(u, bot)
    elif u.is_text(BotCommand.HELP):
        await command_help(u, bot)
    elif u.is_text(BotCommand.NUMBERS_STUDY):
        await command_numbers_study(u, bot)
    elif u.is_text(BotCommand.NUMBERS_TEST):
        await command_numbers_test(u, bot)
    elif status == ChatStatus.PROCESSING:
        await processing(u, bot)
    elif status == ChatStatus.STUDYING_LESSON:
        await lesson_progress(u, bot)
    elif u.is_text(BotKeyboardButton.TAKE_A_LESSON):
        await start_select_lesson_flow(u, bot)
    elif u.is_text(BotKeyboardButton.CHANGE_VOICE_LANGUAGE):
        await start_change_voice_language_flow(u, bot)
    else:
        await sound_text(u, bot)
    Transaction.commit()


async def handle_callback(update: Update, context: CallbackContext):
    Transaction.open()
    u = UpdateAdapter(update)
    bot = context.bot

    await change_voice_language(u, bot)
    await select_lesson(u, bot)
    Transaction.commit()


async def error_handler(update, context: Union[CallbackContext, Any]):
    logging.error("Exception while handling an update:", exc_info=context.error)
    Transaction.rollback()
    await context.bot.send_message(UpdateAdapter(update).chat_id, "error")
