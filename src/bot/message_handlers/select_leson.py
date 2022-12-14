from lazy_streams import stream
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.UpdateAdapter import UpdateAdapter
from src.bot.bot_commands import BotInMessageButton
from src.bot.message_handlers.lesson_progress import start_lesson
from src.db import basic_words_db
from src.db.basic_words_db import WordGroup, PAGE_SIZE

CALLBACK_PREFIX: str = "SELECT_LESSON_"


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
        text_list.append(f"{wg.ord}. {wg.title} {'✅' if wg.was_success else ''}")
    if has_next:
        text_list.append("...")
    return "\n".join(text_list)


def __prepare_message_reply_markup(word_groups: list[WordGroup], has_previous: bool, has_next: bool, page: int):
    inline_buttons = stream(word_groups) \
        .map(lambda x: [InlineKeyboardButton(x.title, callback_data=CALLBACK_PREFIX + x.title)]) \
        .to_list()
    if has_previous:
        inline_buttons.insert(
            0,
            [InlineKeyboardButton("<<", callback_data=CALLBACK_PREFIX + BotInMessageButton.PAGE.value + str(page - 1))])
    if has_next:
        inline_buttons.append(
            [InlineKeyboardButton(">>", callback_data=CALLBACK_PREFIX + BotInMessageButton.PAGE.value + str(page + 1))])
    inline_buttons.append(
        [InlineKeyboardButton("❌", callback_data=CALLBACK_PREFIX + BotInMessageButton.CANCEL.value)])
    return InlineKeyboardMarkup(inline_buttons)


def __select_word_groups(chat_id: int, page: int):
    word_groups: list[WordGroup] = basic_words_db.select_word_groups(chat_id, page)
    has_previous = page != 0
    has_next = len(word_groups) > PAGE_SIZE
    if has_next:
        word_groups.pop()
    return word_groups, has_previous, has_next


def __prepare_message(chat_id: int, page: int = 0) -> tuple[str, InlineKeyboardMarkup]:
    word_groups, has_previous, has_next = __select_word_groups(chat_id, page)

    text = __prepare_message_text(word_groups, has_previous, has_next)
    reply_markup = __prepare_message_reply_markup(word_groups, has_previous, has_next, page)
    return text, reply_markup


async def start_select_lesson_flow(u: UpdateAdapter, bot: Bot):
    text, reply_markup = __prepare_message(u.chat_id)
    await bot.send_message(u.chat_id, text, "markdown", reply_markup=reply_markup)


async def select_lesson(u: UpdateAdapter, bot: Bot):
    if not u.text.startswith(CALLBACK_PREFIX):
        return

    split_text = u.text[len(CALLBACK_PREFIX):]
    if split_text == BotInMessageButton.CANCEL.value:
        await bot.edit_message_text("❌ Yor have cancel lesson selection", u.chat_id, u.original_message_id)
    elif split_text.startswith(BotInMessageButton.PAGE.value):
        new_page = int(split_text[len(BotInMessageButton.PAGE.value):])
        new_text, reply_markup = __prepare_message(u.chat_id, new_page)
        await bot.edit_message_text(new_text,
                                    u.chat_id,
                                    u.original_message_id,
                                    reply_markup=reply_markup,
                                    parse_mode="markdown")
    else:
        await start_lesson(u, bot, split_text)
