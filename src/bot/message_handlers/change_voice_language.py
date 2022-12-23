from lazy_streams import stream
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import BotInMessageButton
from src.db import chat_db, language_db

callback_prefix: str = "CHANGE_VOICE_LANGUAGE_"


async def start_change_voice_language_flow(u: UpdateAdapter, bot: Bot):
    languages = language_db.find_all()

    inline_buttons = stream(list(zip(languages[::2], languages[1::2]))) \
        .map(lambda x: [InlineKeyboardButton(x[0].name, callback_data=callback_prefix + x[0].name),
                        InlineKeyboardButton(x[1].name, callback_data=callback_prefix + x[1].name)]) \
        .to_list()
    inline_buttons.append([InlineKeyboardButton("❌", callback_data=callback_prefix + BotInMessageButton.CANCEL.value)])

    await bot.send_message(u.chat_id,
                           f"I am support {len(languages)} languages.\nSelect the language you want to change to:",
                           reply_markup=InlineKeyboardMarkup(inline_buttons))


async def change_voice_language(u: UpdateAdapter, bot: Bot):
    if u.text == callback_prefix + BotInMessageButton.CANCEL.value:
        await bot.edit_message_text("❌ Yor have cancel language selection", u.chat_id, u.original_message_id)
        return
    db_language = language_db.find_by_name(u.text[len(callback_prefix):])
    await bot.edit_message_text(f"Yor have successful changed language on: _{db_language.name}_",
                                u.chat_id,
                                u.original_message_id,
                                parse_mode="markdown")
    chat_db.update_language_code(u.chat_id, db_language.code)
