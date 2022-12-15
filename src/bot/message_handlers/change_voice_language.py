from lazy_streams import stream
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard, BotCommand
from src.db import chat_db, language_db
from src.db.chat_db import ChatStatus


async def start_change_voice_language_flow(update: Update, context: CallbackContext):
    languages = language_db.find_all()
    await context.bot.send_message(bot_util.chat_id(update),
                                   f"I am support {len(languages)} languages.",
                                   reply_markup=ReplyKeyboardRemove())

    inline_buttons = stream(list(zip(languages[::2], languages[1::2]))) \
        .map(lambda x: [InlineKeyboardButton(x[0].name, None, x[0].name),
                        InlineKeyboardButton(x[1].name, None, x[1].name)]) \
        .to_list()
    inline_buttons.append([InlineKeyboardButton("❌", callback_data=BotCommand.CANCEL.value)])
    await context.bot.send_message(bot_util.chat_id(update),
                                   "Select language you want to change:",
                                   reply_markup=InlineKeyboardMarkup(inline_buttons))
    chat_db.update_status(bot_util.chat_id(update), ChatStatus.EXPECT_LANGUAGE_OF_VOICE_TO_SET)


async def change_voice_language(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    text = bot_util.text(update)
    if text == BotCommand.CANCEL.value:
        chat_db.update_status(chat_id, ChatStatus.NONE)
        return
    like = language_db.find_all_by_name_like(text)
    if len(like) == 0:
        await context.bot.send_message(chat_id=chat_id, text="I am sorry, can not find match language")
    elif len(like) == 1:
        await context.bot.send_message(chat_id=chat_id,
                                       text="Yor successful language changed on " + like[0].name,
                                       reply_markup=home_keyboard)
        chat_db.update_language_code(chat_id, like[0].code)
        chat_db.update_status(chat_id, ChatStatus.NONE)
