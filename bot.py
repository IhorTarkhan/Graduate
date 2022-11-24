import logging
import sys

from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import filters, ApplicationBuilder, Application, CallbackContext, CommandHandler, MessageHandler

import db.chat_db as chat_db
from db.chat import Chat
from src.bot import bot_commands
from src.util import logging_config


async def handle_command_start(update: Update, context: CallbackContext):
    chat_db.upsert(update.message.chat_id)
    kb = [
        [KeyboardButton(bot_commands.sound_of_my_text)]
    ]
    kb_markup = ReplyKeyboardMarkup(kb)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=kb_markup)


async def handle_message(update: Update, context: CallbackContext):
    message = update.message
    chat: Chat = chat_db.find_by_id(message.chat_id)
    if chat.last_action == bot_commands.sound_of_my_text:
        logging.info(11)

    if bot_commands.sound_of_my_text == message.text:
        chat_db.update_last_action(message.chat_id, bot_commands.sound_of_my_text)
        await context.bot.send_message(chat_id=message.chat_id,
                                       text="Enter the text you want to sound",
                                       reply_markup=ReplyKeyboardRemove())
    else:
        await context.bot.send_message(chat_id=message.chat_id,
                                       text=message.text,
                                       reply_markup=ReplyKeyboardRemove())


if __name__ == "__main__":
    logging_config()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(CommandHandler("start", handle_command_start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()
