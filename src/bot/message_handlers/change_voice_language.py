from lazy_streams import stream
from telegram import Bot, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import home_keyboard, BotCommand
from src.db import chat_db, language_db
from src.db.chat_db import ChatStatus


async def start_change_voice_language_flow(u: UpdateAdapter, bot: Bot):
    languages = language_db.find_all()
    await bot.send_message(u.chat_id, f"I am support {len(languages)} languages.",
                           reply_markup=ReplyKeyboardRemove())

    inline_buttons = stream(list(zip(languages[::2], languages[1::2]))) \
        .map(lambda x: [InlineKeyboardButton(x[0].name, callback_data=x[0].name),
                        InlineKeyboardButton(x[1].name, callback_data=x[1].name)]) \
        .to_list()
    inline_buttons.append([InlineKeyboardButton("❌", callback_data=BotCommand.CANCEL.value)])

    await bot.send_message(u.chat_id, "Select language you want to change:",
                           reply_markup=InlineKeyboardMarkup(inline_buttons))
    chat_db.update_status(u.chat_id, ChatStatus.EXPECT_LANGUAGE_OF_VOICE_TO_SET)


async def change_voice_language(u: UpdateAdapter, bot: Bot):
    if u.text == BotCommand.CANCEL.value:
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
        return
    like = language_db.find_all_by_name_like(u.text)
    if len(like) == 0:
        await bot.send_message(u.chat_id, "I am sorry, can not find match language")
    elif len(like) == 1:
        await bot.send_message(u.chat_id, "Yor successful language changed on " + like[0].name,
                               reply_markup=home_keyboard)
        chat_db.update_language_code(u.chat_id, like[0].code)
        chat_db.update_status(u.chat_id, ChatStatus.NONE)
