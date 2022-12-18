from telegram import Bot, ReplyKeyboardRemove

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import home_keyboard
from src.db import chat_db
from src.db.chat_db import ChatStatus
from src.service.audio_files import sound_audio


async def sound_text(u: UpdateAdapter, bot: Bot):
    language = chat_db.find_by_id(u.chat_id).language_code
    await bot.send_audio(u.chat_id, sound_audio(language, u.text), reply_markup=home_keyboard)
    chat_db.update_status(u.chat_id, ChatStatus.NONE)


async def start_sound_text_flow(u: UpdateAdapter, bot: Bot):
    await bot.send_message(u.chat_id, "Enter the text you want to sound", reply_markup=ReplyKeyboardRemove())
    chat_db.update_status(u.chat_id, ChatStatus.EXPECT_TEXT_TO_SOUND)
