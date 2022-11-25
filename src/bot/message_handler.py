import os

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

import db.chat_db as chat_db
from audio.download_audio_files import path_of, fetch
from bot.bot_commands import home_keyboard
from db.chat import Chat
from src.bot import bot_commands


async def handle_command_start(update: Update, context: CallbackContext):
    chat_db.upsert(update.message.chat_id)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=home_keyboard)


async def _sound_of_my_text_execute(update: Update, context: CallbackContext):
    chat_db.update_last_action(update.message.chat_id, None)
    language = "en-US"
    if not os.path.exists(path_of(language, update.message.text)):
        await context.bot.send_message(chat_id=update.message.chat_id, text="Processing your request...")
        fetch({language: [update.message.text]})
    await context.bot.send_audio(chat_id=update.message.chat_id,
                                 audio=open(path_of(language, update.message.text), "rb"),
                                 reply_markup=home_keyboard)


async def _sound_of_my_text_handle(update: Update, context: CallbackContext):
    chat_db.update_last_action(update.message.chat_id, bot_commands.sound_of_my_text)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="Enter the text you want to sound",
                                   reply_markup=ReplyKeyboardRemove())


async def _change_voice_language_handle(update: Update, context: CallbackContext):
    pass
    # chat_db.update_last_action(update.message.chat_id, bot_commands.change_voice_language)
    # await context.bot.send_message(chat_id=update.message.chat_id,
    #                                text="Enter the text you want to sound",
    #                                reply_markup=ReplyKeyboardRemove())


async def _echo(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


async def handle_message(update: Update, context: CallbackContext):
    chat: Chat = chat_db.find_by_id(update.message.chat_id)

    if bot_commands.command_start == update.message.text:
        await handle_command_start(update, context)
    elif bot_commands.sound_of_my_text == chat.last_action:
        await _sound_of_my_text_execute(update, context)
    elif bot_commands.sound_of_my_text == update.message.text:
        await _sound_of_my_text_handle(update, context)
    elif bot_commands.change_voice_language == update.message.text:
        await _change_voice_language_handle(update, context)
    else:
        await _echo(update, context)
