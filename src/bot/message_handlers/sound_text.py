from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.db import chat_db
from src.db.chat_db import ChatStatus
from src.service.audio_files import sound_audio


async def sound_text(u: UpdateAdapter, bot: Bot):
    chat_db.update_status(u.chat_id, ChatStatus.PROCESSING)
    language = chat_db.find_by_id(u.chat_id).language_code
    await bot.send_audio(u.chat_id, sound_audio(language, u.text))
    chat_db.update_status(u.chat_id, ChatStatus.NONE)
