from aiogram.types import Message
from loader import dp, db
from utils.codes_base import generate_code


@dp.message_handler(text='Когда бесплатный?')
async def purchase_counter_info(message: Message):
    purchase_counter = 5 - (await db.purchase_counter_request(message.from_user.id))
    reward_counter = await db.reward_counter_request(message.from_user.id)
    await message.answer(f'Бесплатных напитков: <b>{reward_counter}</b>\n'
                         f'Осталось покупок до следующего бесплатного напитка: <b>{purchase_counter}</b>')

@dp.message_handler(text='Получить бесплатный')
async def get_reward_from_user(message: Message):
    if await db.reward_counter_request(message.from_user.id):
        code = generate_code(task='reward', chat_id=message.chat.id, user_id=message.from_user.id)
        await message.answer(f'Назовите этот код бариста: <b>{code}</b>')
    else:
        purchase_counter = 5 - (await db.purchase_counter_request(message.from_user.id))
        await message.answer(f'У вас нет бесплатных напитков\n'
                             f'Осталось покупок до следующего бесплатного напитка: <b>{purchase_counter}</b>')

@dp. message_handler(text='Учесть покупку')
async def add_purchase_from_user(message: Message):
    code = generate_code(task='purchase', chat_id=message.chat.id, user_id=message.from_user.id)
    await message.answer(f'Назовите этот код бариста: <b>{code}</b>')

