from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

import db.chat_db as chat_db
from audio.download_audio import path_to
from db.chat import Chat
from src.bot import bot_commands


async def _sound_of_my_text_execute(update: Update, context: CallbackContext):
    chat_db.update_last_action(update.message.chat_id, None)
    await context.bot.send_message(chat_id=update.message.chat_id, text="Processing your request...")
    kb = [
        [KeyboardButton(bot_commands.sound_of_my_text)]
    ]
    kb_markup = ReplyKeyboardMarkup(kb)
    await context.bot.send_audio(chat_id=update.message.chat_id,
                                 audio=open(path_to("en-US", "abc"), "rb"),
                                 reply_markup=kb_markup)


async def _sound_of_my_text_handle(update: Update, context: CallbackContext):
    chat_db.update_last_action(update.message.chat_id, bot_commands.sound_of_my_text)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="Enter the text you want to sound",
                                   reply_markup=ReplyKeyboardRemove())


async def _echo(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text=update.message.text,
                                   reply_markup=ReplyKeyboardRemove())


async def handle_message(update: Update, context: CallbackContext):
    chat: Chat = chat_db.find_by_id(update.message.chat_id)

    if bot_commands.sound_of_my_text == chat.last_action:
        await _sound_of_my_text_execute(update, context)
    elif bot_commands.sound_of_my_text == update.message.text:
        await _sound_of_my_text_handle(update, context)
    else:
        await _echo(update, context)
