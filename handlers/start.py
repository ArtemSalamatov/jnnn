from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from keyboards.default.admin_kb import admin_keyboard
from keyboards.default.user_kb import user_keyboard
from asyncpg.exceptions import UniqueViolationError

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Вы назначены администратором', reply_markup=admin_keyboard)
    else:
        try:
            await db.add_user(user_id=message.from_user.id,
                              full_name=message.from_user.full_name
                              )
        except UniqueViolationError:
            pass
        await message.answer('Вы добавлены в базу', reply_markup=user_keyboard)
