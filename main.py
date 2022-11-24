import sys

from telegram.ext import filters, ApplicationBuilder, Application, CommandHandler, MessageHandler

from bot.command_handlr import handle_command_start
from bot.message_handlr import handle_message
from db.util import create_all_tables
from src.util import logging_config

if __name__ == "__main__":
    logging_config()
    create_all_tables()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(CommandHandler("start", handle_command_start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.run_polling()
