from enum import Enum

from telegram import ReplyKeyboardMarkup, KeyboardButton


class BotCommand(Enum):
    COMMAND_START = "/start"
    TAKE_A_LESSON = "Take a lesson"
    CHANGE_VOICE_LANGUAGE = "Change voice language"
    NEXT_PAGE = "NEXT_PAGE"
    PREVIOUS_PAGE = "PREVIOUS_PAGE"
    CANCEL = "CANCEL"


home_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(BotCommand.CHANGE_VOICE_LANGUAGE.value)],
    [KeyboardButton(BotCommand.TAKE_A_LESSON.value)]
])
