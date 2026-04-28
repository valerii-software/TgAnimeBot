from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.callback_data import CallbackAnimeTitle


def get_anime_titles_keyboard(anime_titles: list[tuple[str, int]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for title, title_id in anime_titles:
        builder.button(text=title, callback_data=CallbackAnimeTitle(anime_id=title_id))
    builder.adjust(1)
    return builder.as_markup()


def get_watch_keyboard(player_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Смотреть онлайн", url=player_url)
    ]])
