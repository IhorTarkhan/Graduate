from enum import Enum

from telegram import ReplyKeyboardMarkup, KeyboardButton


class BotCommand(Enum):
    START = "/start"
    HELP = "/help"
    NUMBERS_STUDY = "/numbers_study"
    NUMBERS_TEST = "/numbers_test"


class BotKeyboardButton(Enum):
    TAKE_A_LESSON = "Take a lesson"
    CHANGE_VOICE_LANGUAGE = "Change voice language"


class BotInMessageButton(Enum):
    PAGE = "PAGE"
    CANCEL = "CANCEL"


home_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(BotKeyboardButton.TAKE_A_LESSON.value)],
    [KeyboardButton(BotKeyboardButton.CHANGE_VOICE_LANGUAGE.value)]
])
