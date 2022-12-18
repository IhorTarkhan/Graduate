from enum import Enum

from telegram import Update

from src.bot.bot_commands import BotCommand


class UpdateAdapterType(Enum):
    TEXT = 0
    CALLBACK = 1


class UpdateAdapter:
    def __init__(self, update: Update):
        if update.message is not None:
            self.type: UpdateAdapterType = UpdateAdapterType.TEXT
            message = update.message
            self.chat_id: int = message.chat_id
            self.text: str = message.text
        elif update.callback_query is not None:
            self.type: UpdateAdapterType = UpdateAdapterType.CALLBACK
            callback = update.callback_query
            self.chat_id: int = callback.message.chat_id
            self.text: str = callback.data
        else:
            raise RuntimeError("Unsupported message type: " + update.__str__())

    def is_command(self, bot_command: BotCommand) -> bool:
        return self.text == bot_command.value
