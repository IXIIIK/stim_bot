from config_reader import config

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(massage: types.Message):
    TIMELINE = ["10:00", "11:00",
                "12:00", "13:00", 
                "14:00", "15:00",
                "16:00", "17:00",
                "18:00", "19:00",]

    while True:
        date = datetime.now().strftime('%H:%M')
        if datetime.now().strftime('%H:%M') in TIMELINE:
            await massage.answer(f'это сообщение отправлено в {date}')
        await asyncio.sleep(60)
    
def todo_list():
    buttons = [
        [
            types.InlineKeyboardButton(text='Сделано', callback_data='status_done'),
            types.InlineKeyboardButton(text='Не сделано', callback_data='status_pass')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(Command('check-list'))
async def hi_command(massage: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        )
    )
 

from aiogram import F
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import copy

user_data = {}

CHECK_LIST = {
    'wash': 'помыть раковину',
    'car': 'помыть тачку'
}


class CheckListCallBack(CallbackData, prefix='checklist'):
    do: int

def reset_check_list(user_id):
    user_data[user_id]['to_do'] = copy.deepcopy(CHECK_LIST)



def check_list_button():

    builder = InlineKeyboardBuilder()
    builder.button(
        text='✅', callback_data=CheckListCallBack(do=1)
        )
    builder.button(
        text='❌', callback_data=CheckListCallBack(do=0)
        )
    
    builder.adjust(2)
    return builder.as_markup()

@dp.callback_query(CheckListCallBack.filter())
async def process_checklist_press(callback: CallbackQuery, callback_data: CheckListCallBack):
    final_list = {}
    if callback_data == 1:
        final_list[do] = '✅'
    else:
        final_list[do] = '❌'
    try:
        await callback.message.edit_text(
            text=CHECK_LIST[do],
            reply_markup=check_list_button()
        )
    except TelegramBadRequest:
        pass

    await callback.answer(final_list)



@dp.message(Command('check_list'))
async def check_list_command(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=check_list_button())


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())