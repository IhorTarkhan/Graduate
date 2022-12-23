from enum import Enum

from telegram import ReplyKeyboardMarkup, KeyboardButton


class BotCommand(Enum):
    COMMAND_START = "/start"


class BotKeyboardButton(Enum):
    TAKE_A_LESSON = "Take a lesson"
    CHANGE_VOICE_LANGUAGE = "Change voice language"


class BotInMessageButton(Enum):
    PAGE = "PAGE"
    CANCEL = "CANCEL"


home_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(BotKeyboardButton.CHANGE_VOICE_LANGUAGE.value)],
    [KeyboardButton(BotKeyboardButton.TAKE_A_LESSON.value)]
])
