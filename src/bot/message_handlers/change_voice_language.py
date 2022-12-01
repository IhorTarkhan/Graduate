from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard
from src.db import chat_db
from src.db import language_db
from src.db.chat_db import ChatStatus


async def start_change_voice_language_flow(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="I am support {} languages. Try to type your and i try to find it"
                                   .format(language_db.find_count()),
                                   reply_markup=ReplyKeyboardRemove())
    chat_db.update_status(bot_util.chat_id(update), ChatStatus.EXPECT_LANGUAGE_OF_VOICE_TO_SET)


async def change_voice_language(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    text = bot_util.text(update)
    like = language_db.find_all_by_name_like(text)
    if len(like) == 0:
        await context.bot.send_message(chat_id=chat_id, text="I am sorry, can not find match language")
    elif len(like) == 1:
        chat_db.update_language_code(chat_id, like[0].code)
        await context.bot.send_message(chat_id=chat_id,
                                       text="Yor successful language changed on " + like[0].name,
                                       reply_markup=home_keyboard)
        chat_db.update_status(chat_id, ChatStatus.NONE)
    else:
        keyboard = list(map(lambda x: [InlineKeyboardButton(x.name, callback_data=x.name)], like))
        await context.bot.send_message(chat_id=chat_id,
                                       text="Find next languages by your query:",
                                       reply_markup=(InlineKeyboardMarkup(keyboard)))
