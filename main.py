import logging
import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler, CallbackQueryHandler

from src.bot.message_handler import handle_message
from src.db import __util as db_util
from src.db.chat_db import Chat
from src.db.language_db import Language
from src.db.words_groups_db import WordsGroups
from src.download_languages import download_languages
from src.download_word_groups import download_word_groups


def __setup():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s.%(msecs)03d %(name)25s [%(threadName)25s] %(levelname)7s : %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    db_util.change(Chat.__doc__)
    db_util.change(Language.__doc__)
    db_util.change(WordsGroups.__doc__)

    download_languages()
    download_word_groups()


if __name__ == "__main__":
    __setup()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_handler(CallbackQueryHandler(handle_message))

    application.run_polling()
