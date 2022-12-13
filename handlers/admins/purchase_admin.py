from aiogram.types import Message
from loader import db, dp, bot
from utils.admin_func import add_purchase, get_reward
from utils.codes_base import CODES_BASE

@dp.message_handler(text='INFO')
async def temp_info(message: Message):
    await message.answer(text=str(CODES_BASE))

@dp.message_handler()
async def get_codes(message: Message):
    if message.text in CODES_BASE:
        if CODES_BASE[message.text][0] == 'purchase':
            await add_purchase(message, bot, db)
        elif CODES_BASE[message.text][0] == 'reward':
            await get_reward(message, bot, db)
    else:
        await message.answer('Такого кода не существует')

