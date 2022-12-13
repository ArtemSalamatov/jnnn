from aiogram.types import Message
from utils.codes_base import CODES_BASE


async def add_purchase(message: Message, bot, db):
    await db.add_purchase_to_db(amount=1, user_id=CODES_BASE[message.text][2])
    chat_id = CODES_BASE[message.text][1]
    if await db.add_reward_auto(user_id=CODES_BASE[message.text][2]):
        await bot.send_message(chat_id, 'Ваша покупка учтена, вам начислен бесплатный напиток')
        await message.answer('Покупка учтена, гостю начислен бесплатный напиток')
    else:
        await bot.send_message(chat_id, 'Ваша покупка учтена')
        await message.answer('Покупка учтена')
    CODES_BASE.pop(message.text)

async def get_reward(message: Message, bot, db):
    await db.get_reward_from_db(user_id=CODES_BASE[message.text][2])
    chat_id = CODES_BASE[message.text][1]
    await message.answer('Награда списана')
    await bot.send_message(chat_id, 'Ваша награда списана')
    CODES_BASE.pop(message.text)

