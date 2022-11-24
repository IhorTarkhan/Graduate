from telegram import ReplyKeyboardMarkup, Update, KeyboardButton
from telegram.ext import CallbackContext

import db.chat_db as chat_db
from src.bot import bot_commands


async def handle_command_start(update: Update, context: CallbackContext):
    chat_db.upsert(update.message.chat_id)
    kb = [
        [KeyboardButton(bot_commands.sound_of_my_text)]
    ]
    kb_markup = ReplyKeyboardMarkup(kb)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=kb_markup)
