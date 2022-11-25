from telegram import ReplyKeyboardMarkup, KeyboardButton

command_start = "/start"
sound_of_my_text = "Sound of my text"
change_voice_language = "Change voice language"

home_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(sound_of_my_text)],
    [KeyboardButton(change_voice_language)]
])
