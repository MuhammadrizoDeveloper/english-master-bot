import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordLookup import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = '5542824766:AAGFoLWmKX655ScVdHdlHTkgZamRkR6o9ik'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("English Master botiga xush kelibsiz!\nBotdan foydalanish uchun so‘z yoki matn yuboring.\nDasturchi: @muhammadrizodev")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer("Buyruqlar:\n- /start - Botdan foydalinishni boshlash\n- /help - ushbu xabarni qayta chiqarish\n\nBotdan foydalanish uchun so‘z yuboring.\nDasturchi: @muhammadrizodev\nSource code: https://github.com/MuhammadrizoDeveloper/uzimlo_bot")

@dp.message_handler()
async def tarjimon(message: types.Message):
    try:
        lang = translator.detect(message.text).lang
        if len(message.text.split()) > 2:
            dest = 'uz' if lang == 'en' else 'en'
            await message.answer(translator.translate(message.text, dest).text)
        else:
            if lang=='en':
                word_id = message.text
            else:
                word_id = translator.translate(message.text, dest='en').text

            lookup = getDefinitions(word_id)
            if lookup:
                await message.answer(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
                if lookup.get('audio'):
                    await message.answer_voice(lookup['audio'])
            else:
                await message.answer("Bunday so'z topilmadi")
    except KeyError:
        await message.answer("Bunday so'z topilmadi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)