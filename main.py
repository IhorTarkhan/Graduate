import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler, CallbackQueryHandler

from src.bot.message_handler import handle_message
from src.util.start_util import start_util

if __name__ == "__main__":
    start_util()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(CallbackQueryHandler(handle_message))

    application.run_polling()
