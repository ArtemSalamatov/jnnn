from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_callback, rait_callback

choice = InlineKeyboardMarkup(row_width=2)


def create_keyboard(item_id):
    choice = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Купить товар',
                                              callback_data=buy_callback.new(id=item_id)
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Вверх',
                                              callback_data=rait_callback.new(result=1, id=item_id)
                                          ),
                                          InlineKeyboardButton(
                                              text='Вниз',
                                              callback_data=rait_callback.new(result=-0, id=item_id)
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Поделиться с другом',
                                              switch_inline_query=str(item_id)
                                          )
                                      ]
                                  ])
    return choice
