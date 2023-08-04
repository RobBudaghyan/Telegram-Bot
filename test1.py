import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup

# Replace 'YOUR_BOT_TOKEN' with the token provided by BotFather
API_TOKEN = '6145169134:AAF39yuQRrF8q8xWX0V3cQrrEOuFMBB28GQ'

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def on_start_command(message: types.Message):
    phones_data = get_phones_data()
    await message.reply(phones_data)

async def on_help_command(message: types.Message):
    await message.reply("You can use the following commands:\n/start - Start the bot\n/help - Get help")

# Register the command handlers
dp.register_message_handler(on_start_command, commands=["start"])
dp.register_message_handler(on_help_command, commands=["help"])

# Web scraping function to fetch data from the website
def get_phones_data():
    url = "https://www.mobilecentre.am/category/phones/138/0/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup.findAll()
        return soup
        # Add your web scraping logic here to extract data from the website
        # For example, find elements using soup.find() or soup.find_all()

        # Replace the following example with the actual data you want to send in the bot response
        phones_data = "Here is some data from the website:\n"
        phones_data += "Phone 1: Price $500\n"
        phones_data += "Phone 2: Price $600\n"
        phones_data += "Phone 3: Price $700\n"
        return phones_data
    else:
        return "Failed to fetch data from the website."

async def on_phones_command(message: types.Message):
    phones_data = get_phones_data()
    await message.reply(phones_data)

# Register the custom command handler
dp.register_message_handler(on_phones_command, commands=["phones"])

if __name__ == '__main__':
    # Add a logging middleware to get logs from aiogram
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())

    # Start the bot
    executor.start_polling(dp)
