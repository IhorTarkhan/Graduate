import os

from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from src.audio.download_audio_files import path_of, fetch_audio_files
from src.bot import bot_commands
from src.bot.bot_commands import home_keyboard
from src.db import chat_db
from src.db import language_db
from src.util import bot_util


async def handle_command_start(update: Update, context: CallbackContext):
    chat_db.upsert(bot_util.chat_id(update))
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=home_keyboard)


async def _sound_of_my_text_execute(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    language = chat_db.find_by_id(chat_id).language_code
    if not os.path.exists(path_of(language, bot_util.text(update))):
        await context.bot.send_message(chat_id=chat_id, text="Processing your request...")
        fetch_audio_files({language: [bot_util.text(update)]})
    await context.bot.send_audio(chat_id=chat_id,
                                 audio=open(path_of(language, bot_util.text(update)), "rb"),
                                 reply_markup=home_keyboard)
    chat_db.update_last_action(chat_id, None)


async def _sound_of_my_text_handle(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="Enter the text you want to sound",
                                   reply_markup=ReplyKeyboardRemove())
    chat_db.update_last_action(bot_util.chat_id(update), bot_commands.sound_of_my_text)


async def _change_voice_language_handle(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="I am support {} languages. Try to type your and i try to find it"
                                   .format(language_db.find_count()),
                                   reply_markup=ReplyKeyboardRemove())
    chat_db.update_last_action(bot_util.chat_id(update), bot_commands.change_voice_language)


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
        chat_db.update_last_action(chat_id, None)
    else:
        keyboard = list(map(lambda x: [InlineKeyboardButton(x.name, callback_data=x.name)], like))
        await context.bot.send_message(chat_id=chat_id,
                                       text="Find next languages by your query:",
                                       reply_markup=(InlineKeyboardMarkup(keyboard)))


async def _echo(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=bot_util.chat_id(update), text=bot_util.text(update))


async def handle_message(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    text = bot_util.text(update)
    chat: chat_db.Chat = chat_db.find_by_id(chat_id)
    last_action = chat.last_action

    if text == bot_commands.command_start:
        await handle_command_start(update, context)
    elif last_action == bot_commands.sound_of_my_text:
        await _sound_of_my_text_execute(update, context)
    elif last_action == bot_commands.change_voice_language:
        await _change_voice_language_execute(update, context)
    elif text == bot_commands.sound_of_my_text:
        await _sound_of_my_text_handle(update, context)
    elif text == bot_commands.change_voice_language:
        await _change_voice_language_handle(update, context)
    else:
        await _echo(update, context)
