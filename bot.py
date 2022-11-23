import logging
from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import filters, ApplicationBuilder, Application, CallbackContext, CommandHandler, MessageHandler
import sys


async def start(update: Update, context: CallbackContext):
    kb = [[KeyboardButton("/command1")],
          [KeyboardButton("/command2")]]
    kb_markup = ReplyKeyboardMarkup(kb)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=kb_markup)


async def echo(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=update.message.text,
                                   reply_markup=ReplyKeyboardRemove())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)25s - %(levelname)8s - %(message)s")
    logging.info("stat")

    application: Application = ApplicationBuilder().token(sys.argv[1]).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
