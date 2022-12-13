from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Учесть покупку')
        ],
        [
            KeyboardButton(text='Когда бесплатный?')
        ],
        [
            KeyboardButton(text='Получить бесплатный')
        ]
    ],
    resize_keyboard=True
)
