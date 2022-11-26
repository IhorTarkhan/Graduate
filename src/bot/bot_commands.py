from enum import Enum

from telegram import ReplyKeyboardMarkup, KeyboardButton


class BotCommand(Enum):
    COMMAND_START = "/start"
    SOUND_OF_MY_TEXT = "Sound of my text"
    CHANGE_VOICE_LANGUAGE = "Change voice language"


home_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(BotCommand.SOUND_OF_MY_TEXT.value)],
    [KeyboardButton(BotCommand.CHANGE_VOICE_LANGUAGE.value)]
])
