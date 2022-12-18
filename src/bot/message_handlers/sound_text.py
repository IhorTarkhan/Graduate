from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard
from src.db import chat_db
from src.db.chat_db import ChatStatus
from src.download.audio_files import sound_audio


async def sound_text(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    language = chat_db.find_by_id(chat_id).language_code
    text = bot_util.text(update)
    await context.bot.send_audio(chat_id, sound_audio(language, text), reply_markup=home_keyboard)
    chat_db.update_status(chat_id, ChatStatus.NONE)


async def start_sound_text_flow(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    await context.bot.send_message(chat_id, "Enter the text you want to sound", reply_markup=ReplyKeyboardRemove())
    chat_db.update_status(chat_id, ChatStatus.EXPECT_TEXT_TO_SOUND)
