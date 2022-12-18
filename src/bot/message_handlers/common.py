from telegram import Update
from telegram.ext import CallbackContext

from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard
from src.db import chat_db


async def command_start(update: Update, context: CallbackContext):
    chat_db.upsert(bot_util.chat_id(update))
    await context.bot.send_message(bot_util.chat_id(update), "I'm a bot, please talk to me!",
                                   reply_markup=home_keyboard)


async def processing(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    await context.bot.send_message(chat_id, "Please wait, processing your previous request...")


async def can_not_understand_you(update: Update, context: CallbackContext):
    await context.bot.send_message(bot_util.chat_id(update), "Sorry, I can't understand you")
