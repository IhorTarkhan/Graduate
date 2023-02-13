from enum import Enum

from telegram import ReplyKeyboardMarkup, KeyboardButton


class BotCommand(Enum):
    START = "/start"
    HELP = "/help"
    NUMBERS_STUDY = "/numbers_study"
    NUMBERS_TEST = "/numbers_test"

    def help(self) -> str:
        if self == BotCommand.START:
            return """
/start - remove bot state (progres of lesson or studying) and clear all data about user in bot database"""
        elif self == BotCommand.HELP:
            return """
/help - show this help message"""
        elif self == BotCommand.NUMBERS_STUDY:
            return """
/numbers_study [number (integer)] - start sending you audio files with titles of numbers between number you enter and 0

/numbers_study [number from (integer)] [number to (integer)] - start sending you audio files with titles of numbers 
between numbers you enter"""
        elif self == BotCommand.NUMBERS_TEST:
            return """
/numbers_test [number (integer)] - start sending you audio files of numbers between number you enter and 0 and you have 
to enter the value of this number

/numbers_test [number from (integer)] [number to (integer)] - start sending you audio files of numbers between numbers 
you enter and you have to enter the value of this number
"""


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
