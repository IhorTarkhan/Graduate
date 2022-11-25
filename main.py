import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler

from src.bot.message_handler import handle_message
from src.util.db_util import create_all_tables
from src.util.log_util import logging_config

if __name__ == "__main__":
    logging_config()
    create_all_tables()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    application.run_polling()
