import logging
import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler, CallbackQueryHandler

from src.bot.message_handler import handle_text, handle_callback, error_handler
from src.db.Transaction import Transaction
from src.db.basic_words_db import BasicWords
from src.db.chat_db import Chat
from src.db.language_db import Language
from src.db.lesson_progress_db import LessonProgress
from src.service.basic_languages import insert_basic_languages
from src.service.basic_words import download_basic_words


def __setup():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s.%(msecs)03d %(levelname)7s : %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    Transaction.open()
    Transaction.change(Chat.CREATE_SCRIPT)
    Transaction.change(Language.CREATE_SCRIPT)
    Transaction.change(BasicWords.CREATE_SCRIPT)
    Transaction.change(LessonProgress.CREATE_SCRIPT)

    insert_basic_languages()
    download_basic_words()
    Transaction.commit()


if __name__ == "__main__":
    __setup()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_error_handler(error_handler)

    application.run_polling()
