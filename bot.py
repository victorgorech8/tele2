import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters import Command
from datetime import datetime
from aiogram import html
import re
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
import pathlib
import shutil
import os
import pandas
from aiogram.utils.keyboard import ReplyKeyboardBuilder
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6545031202:AAF7GBzCuLxv32_KUbqx2hri141vdTZjwbU")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>, пришли мне файл!",
        parse_mode=ParseMode.HTML)




@dp.message(F.document)
async def download_file(message: Message, bot: Bot,mylist: set[str]):
    os.remove("C:/Users/victo/Documents/telebot/piwe.xlsx")
    await bot.download(
        message.document,
        destination=f"C:/Users/victo/Documents/telebot/piwe.xlsx"
    )
    data=pandas.read_excel(io='piwe.xlsx', engine='openpyxl')
    ocenka=len(data)-1
    for i in range(ocenka+1):
        mylist.add(data['Группа'].values[i])

    builder = ReplyKeyboardBuilder()
    for i in mylist:
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите  группу:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text)
async def echo_with_time(message: Message):
    data=pandas.read_excel(io='piwe.xlsx', engine='openpyxl')
    ocenka=len(data)-1
    k=0
    a=set()
    b=set()
    c=set()
    for i in range(ocenka+1):
        if data['Группа'].values[i]==message.text:
            k+=1
            a.add(data['Личный номер студента'].values[i])
            b.add(data['Уровень контроля'].values[i])
            c.add(data['Год'].values[i])

    await message.answer(f"Исходном датасете содеражалось {ocenka} оценок, из них {k} относиться к группе {message.text}\n\n Исходном датасете находится {len(a)} судентасо слудующими личными номерами:{a}\n\n Используемый формы контроля: {b}\n\n Данные пресдставлены за по следующим учебным годам:{c}", parse_mode="HTML")
    
    

async def main():
    await dp.start_polling(bot, mylist=set() )

if __name__ == "__main__":
    asyncio.run(main())
