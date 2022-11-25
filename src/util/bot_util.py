from telegram import Update


def chat_id(update: Update) -> int:
    if update.message is not None:
        return update.message.chat_id
    elif update.callback_query is not None:
        return update.callback_query.message.chat_id
    else:
        raise RuntimeError("Unsupported message type: " + update.__str__())


def text(update: Update) -> str:
    if update.message is not None:
        return update.message.text
    elif update.callback_query is not None:
        return update.callback_query.data
    else:
        raise RuntimeError("Unsupported message type: " + update.__str__())
