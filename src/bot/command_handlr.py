from telegram import Update
from telegram.ext import CallbackContext

import db.chat_db as chat_db
from bot.bot_commands import home_keyboard


async def handle_command_start(update: Update, context: CallbackContext):
    chat_db.upsert(update.message.chat_id)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=home_keyboard)
