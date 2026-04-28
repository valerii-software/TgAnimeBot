import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.utils.utils import (
    search_releases, get_anime_titles, get_poster_url, get_external_player_url,
)
from core.keyboards.inline import get_anime_titles_keyboard, get_watch_keyboard
from core.utils.callback_data import CallbackAnimeTitle
from core.utils.states import StepsAnime

router = Router()


@router.message(Command("search"))
async def get_search(message: Message, state: FSMContext):
    await message.answer(text="<b>Введите название аниме:</b>", parse_mode="HTML")
    await state.set_state(StepsAnime.ANIME_NAME)


@router.message(StepsAnime.ANIME_NAME)
async def get_found_anime(message: Message, state: FSMContext):
    await state.set_state(None)  # clear state but keep data
    try:
        releases = await search_releases(user_input=message.text)
        if not releases:
            await message.answer(text="<b>Ничего не найдено 😿</b>", parse_mode="HTML")
            return
        # store releases in state data for later retrieval by ID
        await state.update_data(releases={str(r["id"]): r for r in releases})
        anime_titles = get_anime_titles(releases)
        await message.answer(text="Вот что удалось найти:", reply_markup=get_anime_titles_keyboard(anime_titles))
    except Exception:
        logging.exception("Error in get_found_anime")
        await message.answer(text="<b>Ошибка при поиске. Попробуйте позже.</b>", parse_mode="HTML")


@router.callback_query(CallbackAnimeTitle.filter())
async def get_anime(call: CallbackQuery, callback_data: CallbackAnimeTitle, state: FSMContext):
    try:
        data = await state.get_data()
        release = data.get("releases", {}).get(str(callback_data.anime_id))
        if not release:
            await call.answer("Данные устарели. Выполните поиск заново.", show_alert=True)
            return

        name = release["name"]["main"]
        description = release.get("description") or "Нет описания"
        genres = ", ".join(g["name"] for g in release.get("genres", []))
        episodes_total = release.get("episodes_total")
        episodes_str = str(episodes_total) if episodes_total else "Нет данных"

        header = "\n".join([
            f"<b>Жанр:</b> {genres}",
            f"<b>Название:</b> {name}",
            f"<b>Серий:</b> {episodes_str}",
            "<b>Описание:</b> ",
        ])
        max_desc = 1024 - len(header) - 3  # 3 for "..."
        if len(description) > max_desc:
            description = description[:max_desc] + "..."
        caption = header + description

        player_url = get_external_player_url(release)
        keyboard = get_watch_keyboard(player_url) if player_url else None

        await call.message.answer_photo(
            photo=get_poster_url(release),
            caption=caption,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    except Exception:
        logging.exception("Error in get_anime")
        await call.answer("Ошибка при загрузке аниме. Попробуйте позже.", show_alert=True)
