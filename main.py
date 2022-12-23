import logging
import sys

from telegram.ext import filters, ApplicationBuilder, Application, MessageHandler, CallbackQueryHandler

from src.bot.message_handler import handle_text, handle_callback
from src.db import __util as db_util
from src.db.basic_words_db import BasicWords
from src.db.chat_db import Chat
from src.db.language_db import Language
from src.db.lesson_attempt_db import LessonAttempt
from src.db.lesson_progress_db import LessonProgress
from src.service.basic_words import download_basic_words
from src.service.basic_languages import insert_basic_languages


def __setup():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s.%(msecs)03d %(levelname)7s : %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    db_util.change(Chat.CREATE_SCRIPT)
    db_util.change(Language.CREATE_SCRIPT)
    db_util.change(BasicWords.CREATE_SCRIPT)
    db_util.change(LessonAttempt.CREATE_SCRIPT)
    db_util.change(LessonProgress.CREATE_SCRIPT)

    insert_basic_languages()
    download_basic_words()


if __name__ == "__main__":
    __setup()

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.add_handler(CallbackQueryHandler(handle_callback))

    application.run_polling()
