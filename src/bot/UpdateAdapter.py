from enum import Enum

from telegram import Update


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
            original_message = callback.message
            self.chat_id: int = original_message.chat_id
            self.text: str = callback.data
            self.original_message_id: int = original_message.message_id
        else:
            raise ValueError("Unsupported message type: " + update.__str__())

    def is_text(self, bot_command: Enum) -> bool:
        return self.type == UpdateAdapterType.TEXT and self.text == bot_command.value

    def is_text_start_with(self, bot_command: Enum) -> bool:
        return self.type == UpdateAdapterType.TEXT and self.text.startswith(bot_command.value)
