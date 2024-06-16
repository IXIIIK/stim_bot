#from config_reader import config

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime


logging.basicConfig(level=logging.INFO)
#bot = Bot(token=config.bot_token.get_secret_value())
bot = Bot(token='7109783097:AAHnTQZoU4x3qS8vfF26EqpckEdxtYI9olQ')
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(massage: types.Message):
    TIMELINE = ["10:00", "11:00",
                "12:00", "13:00", 
                "14:00", "15:00",
                "16:00", "17:00",
                "18:00", "19:00", "20:36"]

    while True:
        date = datetime.now().strftime('%H:%M')
        if datetime.now().strftime('%H:%M') in TIMELINE:
            await massage.answer(f'это сообщение отправлено в {date}')
        await asyncio.sleep(60)
    
@dp.message(Command('hi'))
async def hi_command(massage: types.Message):
    await massage.answer(f'Привет')
    



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())