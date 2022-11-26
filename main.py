import logging
import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler, CallbackQueryHandler

from src.bot.message_handler import handle_message
from src.db.chat_db import Chat
from src.db.language_db import Language
from src.db import __util as db_util


def _setup():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)25s - %(levelname)8s - %(message)s")

    db_util.change(Chat.__doc__)
    db_util.change(Language.__doc__)


if __name__ == "__main__":
    _setup()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(CallbackQueryHandler(handle_message))

    application.run_polling()
