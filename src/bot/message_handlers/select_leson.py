from typing import Optional

from lazy_streams import stream
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Message
from telegram.ext import CallbackContext

from src.bot import __util as bot_util
from src.bot.bot_commands import BotCommand
from src.bot.message_handlers.lesson_progress import start_lesson
from src.db import basic_words_db, chat_db, language_selector_state_db
from src.db.basic_words_db import WordGroup, PAGE_SIZE
from src.db.chat_db import ChatStatus


def __prepare_message_text(word_groups: list[WordGroup], has_previous: bool, has_next: bool):
    last_level_name: str = word_groups[0].level_name
    text_list: list[str] = ["_Select lesson:_", "", f"*{last_level_name.upper()}:*"]
    if has_previous:
        text_list.append("...")
    for wg in word_groups:
        if wg.level_name != last_level_name:
            last_level_name = wg.level_name
            text_list.append("")
            text_list.append(f"*{last_level_name.upper()}*:")
        text_list.append(f"{wg.ord}. {wg.title}")
    if has_next:
        text_list.append("...")
    return "\n".join(text_list)


def __prepare_message_reply_markup(word_groups: list[WordGroup], has_previous: bool, has_next: bool):
    inline_buttons = stream(word_groups).map(lambda x: [InlineKeyboardButton(x.title, callback_data=x.title)]).to_list()
    if has_previous:
        inline_buttons.insert(0, [InlineKeyboardButton("<<", callback_data=BotCommand.PREVIOUS_PAGE.value)])
    if has_next:
        inline_buttons.append([InlineKeyboardButton(">>", callback_data=BotCommand.NEXT_PAGE.value)])
    inline_buttons.append([InlineKeyboardButton("❌", callback_data=BotCommand.CANCEL.value)])
    return InlineKeyboardMarkup(inline_buttons)


def __select_word_groups(page):
    word_groups: list[WordGroup] = basic_words_db.select_word_groups(page)
    has_previous = page != 0
    has_next = len(word_groups) > PAGE_SIZE
    if has_next:
        word_groups.pop()
    return word_groups, has_previous, has_next


def __prepare_message(page: int = 0) -> tuple[str, InlineKeyboardMarkup]:
    word_groups, has_previous, has_next = __select_word_groups(page)

    text = __prepare_message_text(word_groups, has_previous, has_next)
    reply_markup = __prepare_message_reply_markup(word_groups, has_previous, has_next)
    return text, reply_markup


async def start_select_lesson_flow(update: Update, context: CallbackContext):
    text, reply_markup = __prepare_message()
    message: Message = await context.bot.send_message(chat_id=bot_util.chat_id(update),
                                                      text=text,
                                                      reply_markup=reply_markup,
                                                      parse_mode="markdown")
    chat_db.update_status(bot_util.chat_id(update), ChatStatus.EXPECT_SELECT_LESSON)
    language_selector_state_db.save(bot_util.chat_id(update), message.message_id, 0)


async def select_lesson(update: Update, context: CallbackContext):
    chat_id = bot_util.chat_id(update)
    text = bot_util.text(update)
    language_selector_state = language_selector_state_db.select_by_chat(chat_id)
    if text == BotCommand.CANCEL.value:
        await context.bot.edit_message_text("_You have cancel selection_",
                                            language_selector_state.chat_id,
                                            language_selector_state.message_id,
                                            parse_mode="markdown")
        chat_db.update_status(chat_id, ChatStatus.NONE)
    elif text == BotCommand.NEXT_PAGE.value or text == BotCommand.PREVIOUS_PAGE.value:
        if text == BotCommand.NEXT_PAGE.value:
            language_selector_state_db.increase_page(chat_id)
            new_text, reply_markup = __prepare_message(language_selector_state.current_page + 1)
        else:
            language_selector_state_db.decrease_page(chat_id)
            new_text, reply_markup = __prepare_message(language_selector_state.current_page - 1)
        await context.bot.edit_message_text(new_text,
                                            language_selector_state.chat_id,
                                            language_selector_state.message_id,
                                            reply_markup=reply_markup,
                                            parse_mode="markdown")
    else:
        word_groups, _, _ = __select_word_groups(language_selector_state.current_page)
        selected: Optional[str] = None
        for wg in word_groups:
            if wg.title.lower() == text.lower():
                selected = wg.title
                break
        if selected is not None:
            await context.bot.edit_message_text(f"You select *{selected}*",
                                                language_selector_state.chat_id,
                                                language_selector_state.message_id,
                                                parse_mode="markdown")
            chat_db.update_status(chat_id, ChatStatus.STUDYING_LESSON)
            await start_lesson(chat_id, selected, context)
        else:
            await context.bot.send_message(chat_id=chat_id, text="Please select value above or cancel")
