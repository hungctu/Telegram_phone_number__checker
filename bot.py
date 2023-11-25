import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ParseMode
from aiogram.types.force_reply import ForceReply
from config import *

from phone_validation import user_validator, client_telegram, message_telegram

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','menu'])
async def start(message: types.Message):
    await message.answer('Please enter the phone number you want to check',
                         reply_markup=ForceReply(),
                         parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_txt_file(message: types.Message):
    global phone
    document = message.document
    if document.mime_type == "text/plain":
        # Download the file
        file_id = document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        await bot.download_file(file_path, f"downloaded.txt")

        # Read the content of the downloaded file
        with open("downloaded.txt", "r") as txt_file:
            file_contents = txt_file.read()
            word = file_contents.split('\n')

        print(word)
        phone = await message_telegram(word)
        # print(f'PHONE : {phone}')
        # phone = await client_telegram(file_contents)
        # for i in word:
        #     phone = await client_telegram(i)
        #     print(f'PHONE : {phone[i]}')
        #     stri += str(phone[i]) + '\n'
        # Respond with the file contents
        await message.answer(phone, parse_mode=ParseMode.MARKDOWN)



def main():
    executor.start_polling(dp, skip_updates=True)
