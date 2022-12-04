import logging
import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler, CallbackQueryHandler

from src.bot.message_handler import handle_message
from src.db import __util as db_util
from src.db.chat_db import Chat
from src.db.language_db import Language
from src.db.basic_words_db import BasicWords
from src.download.languages import download_languages
from src.download.basic_words import download_basic_words


def __setup():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s.%(msecs)03d %(levelname)7s : %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    db_util.change(Chat.CREATE_SCRIPT)
    db_util.change(Language.CREATE_SCRIPT)
    db_util.change(BasicWords.CREATE_SCRIPT)

    download_languages()
    download_basic_words()


if __name__ == "__main__":
    __setup()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(CallbackQueryHandler(handle_message))

    application.run_polling()
