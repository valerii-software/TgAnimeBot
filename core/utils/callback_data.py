from aiogram.filters.callback_data import CallbackData


class CallbackAnimeTitle(CallbackData, prefix="anime_title"):
    anime_id: int
