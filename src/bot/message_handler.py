import logging

from telegram import Update
from telegram.ext import CallbackContext

from src.bot import __util as bot_util
from src.bot.bot_commands import home_keyboard, BotCommand
from src.bot.message_handlers.change_voice_language import change_voice_language, start_change_voice_language_flow
from src.bot.message_handlers.select_leson import start_select_lesson_flow, select_lesson
from src.bot.message_handlers.sound_text import sound_text, start_sound_text_flow
from src.db import chat_db
from src.db.chat_db import Chat, ChatStatus


async def __command_start(update: Update, context: CallbackContext):
    chat_db.upsert(bot_util.chat_id(update))
    await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                   text="I'm a bot, please talk to me!",
                                   reply_markup=home_keyboard)


async def __processing(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    await context.bot.send_message(chat_id=chat_id, text="Please wait, processing your previous request...")


async def __echo(update: Update, context: CallbackContext):
    logging.info("echo")
    await context.bot.send_message(chat_id=bot_util.chat_id(update), text=bot_util.text(update))


async def handle_message(update: Update, context: CallbackContext):
    chat_id: int = bot_util.chat_id(update)
    text: str = bot_util.text(update)
    chat: Chat = chat_db.find_by_id(chat_id)
    status: ChatStatus = chat.status
    if text == BotCommand.COMMAND_START.value:
        await __command_start(update, context)
    elif status == ChatStatus.PROCESSING:
        await __processing(update, context)
    elif status == ChatStatus.EXPECT_TEXT_TO_SOUND:
        await sound_text(update, context)
    elif status == ChatStatus.EXPECT_LANGUAGE_OF_VOICE_TO_SET:
        await change_voice_language(update, context)
    elif status == ChatStatus.EXPECT_SELECT_LESSON:
        await select_lesson(update, context)
    elif text == BotCommand.SOUND_OF_MY_TEXT.value:
        await start_sound_text_flow(update, context)
    elif text == BotCommand.TAKE_A_LESSON.value:
        await start_select_lesson_flow(update, context)
    elif text == BotCommand.CHANGE_VOICE_LANGUAGE.value:
        await start_change_voice_language_flow(update, context)
    else:
        await __echo(update, context)
