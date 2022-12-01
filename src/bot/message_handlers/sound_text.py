import os

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from src.__util import path_of_audio
from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard
from src.db import chat_db
from src.db.chat_db import ChatStatus
from src.download.audio_files import download_audio_file


async def sound_text(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    language = chat_db.find_by_id(chat_id).language_code
    if not os.path.exists(path_of_audio(language, bot_util.text(update))):
        chat_db.update_status(chat_id, ChatStatus.PROCESSING)
        await context.bot.send_message(chat_id=chat_id, text="Processing your request...")
        download_audio_file(language, bot_util.text(update))
    await context.bot.send_audio(chat_id=chat_id,
                                 audio=open(path_of_audio(language, bot_util.text(update)), "rb"),
                                 reply_markup=home_keyboard)
    chat_db.update_status(chat_id, ChatStatus.NONE)


async def start_sound_text_flow(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="Enter the text you want to sound",
                                   reply_markup=ReplyKeyboardRemove())
    chat_db.update_status(bot_util.chat_id(update), ChatStatus.EXPECT_TEXT_TO_SOUND)
