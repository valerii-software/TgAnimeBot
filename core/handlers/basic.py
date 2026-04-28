from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import models
from core.message_texts import get_start_message, vlc_message, help_message, support_message

router = Router()


@router.message(Command("start", "run"))
async def get_start(message: Message, session: AsyncSession):
    existing = await session.scalar(
        select(models.UserData).where(models.UserData.id == message.from_user.id)
    )
    if existing is None:
        session.add(models.UserData(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            date_joined=message.date,
        ))
        await session.commit()
    await message.answer(text=get_start_message, parse_mode="HTML")


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer(text=help_message, parse_mode="HTML")


@router.message(Command("support"))
async def get_support(message: Message):
    await message.answer(text=support_message, parse_mode="HTML")


@router.message(Command("vlc"))
async def get_vlc(message: Message):
    await message.answer(text=vlc_message, parse_mode="HTML")
