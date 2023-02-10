from telegram import Bot

from src.bot.UpdateAdapter import UpdateAdapter
from src.db import chat_db
from src.service.audio_files import sound_audio


async def sound_text(u: UpdateAdapter, bot: Bot):
    language = chat_db.find_by_id(u.chat_id).language.code
    audio_link = sound_audio(language, u.text)
    await bot.send_audio(u.chat_id, audio_link)
