import os

from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.audio.download_audio_files import path_of, fetch_audio_files
from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard, BotCommand
from src.db import chat_db
from src.db import language_db
from src.db.chat_db import Chat, ChatStatus


async def handle_command_start(update: Update, context: CallbackContext):
    chat_db.upsert(bot_util.chat_id(update))
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=home_keyboard)


async def _handle_processing(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    await context.bot.send_message(chat_id=chat_id, text="Please wait, processing your previous request...")


async def _sound_of_my_text_execute(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    language = chat_db.find_by_id(chat_id).language_code
    if not os.path.exists(path_of(language, bot_util.text(update))):
        chat_db.update_status(chat_id, ChatStatus.PROCESSING)
        await context.bot.send_message(chat_id=chat_id, text="Processing your request...")
        fetch_audio_files({language: [bot_util.text(update)]})
    await context.bot.send_audio(chat_id=chat_id,
                                 audio=open(path_of(language, bot_util.text(update)), "rb"),
                                 reply_markup=home_keyboard)
    chat_db.update_status(chat_id, ChatStatus.NONE)


async def _sound_of_my_text_handle(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="Enter the text you want to sound",
                                   reply_markup=ReplyKeyboardRemove())
    chat_db.update_status(bot_util.chat_id(update), ChatStatus.EXPECT_TEXT_TO_SOUND)


async def _change_voice_language_handle(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="I am support {} languages. Try to type your and i try to find it"
                                   .format(language_db.find_count()),
                                   reply_markup=ReplyKeyboardRemove())
    chat_db.update_status(bot_util.chat_id(update), ChatStatus.EXPECT_LANGUAGE_OF_VOICE_TO_SET)


async def _change_voice_language_execute(update: Update, context: CallbackContext):
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


async def _echo(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update), text=bot_util.text(update))


async def handle_message(update: Update, context: CallbackContext):
    chat_id: int = bot_util.chat_id(update)
    text: str = bot_util.text(update)
    chat: Chat = chat_db.find_by_id(chat_id)
    status: ChatStatus = chat.status
    if text == BotCommand.COMMAND_START.value:
        await handle_command_start(update, context)
    elif status == ChatStatus.PROCESSING:
        await _handle_processing(update, context)
    elif status == ChatStatus.EXPECT_TEXT_TO_SOUND:
        await _sound_of_my_text_execute(update, context)
    elif status == ChatStatus.EXPECT_LANGUAGE_OF_VOICE_TO_SET:
        await _change_voice_language_execute(update, context)
    elif text == BotCommand.SOUND_OF_MY_TEXT.value:
        await _sound_of_my_text_handle(update, context)
    elif text == BotCommand.CHANGE_VOICE_LANGUAGE.value:
        await _change_voice_language_handle(update, context)
    else:
        await _echo(update, context)
