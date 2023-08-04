import logging
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define your Telegram bot token here
TOKEN = '6145169134:AAF39yuQRrF8q8xWX0V3cQrrEOuFMBB28GQ'

# Load products from Excel file
PRODUCTS_FILE = r'C:\Users\budag\OneDrive\Рабочий стол\products.xlsx'
products_df = pd.read_excel(PRODUCTS_FILE)





# Global variable to keep track of the current product index
current_product_index = 0

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Start command handler
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Yes", callback_data='show_products'))
    keyboard.add(InlineKeyboardButton("No", callback_data='no_products'))

    menu_button = KeyboardButton("Menu")
    command_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    command_menu.add(menu_button)

    await message.answer("Hey there!\nDo you want to see our products?", reply_markup=keyboard)
    await message.answer("You can also use the menu below.", reply_markup=command_menu)


# Show products
async def show_products(message: types.Message):
    global current_product_index
    if current_product_index < len(products_df):
        product_name = products_df.iloc[current_product_index]['Name']
        product_description = products_df.iloc[current_product_index]['Description']
        product_image_url = products_df.iloc[current_product_index]['Image']

        # Send product name and description
        await message.answer(f"Product: {product_name}\n\n{product_description}")

        # Send image using its URL
        await message.answer_photo(photo=product_image_url)

        # Create keyboard buttons with less transparency (alpha=0.7)
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(InlineKeyboardButton("Buy now!", url=products_df.iloc[current_product_index]['Link'], alpha=0.7))
        keyboard.add(InlineKeyboardButton("Pass", callback_data='pass', alpha=0.7))

        await message.answer("What would you like to do?", reply_markup=keyboard)
    else:
        # When all products are showcased
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Start Over", callback_data='start_over'))

        await message.answer("Products are over! Do you want to start over?", reply_markup=keyboard)


# Button callback handler
@dp.callback_query_handler(text='show_products')
async def button_show_products(query: types.CallbackQuery):
    await query.answer()
    await show_products(query.message)


@dp.callback_query_handler(text='no_products')
async def button_no_products(query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Restart", callback_data='restart', alpha=0.7))

   # await query.answer("Okay, have a good day!", show_alert=True)
    await query.message.answer("Do you want to start from the beginning?", reply_markup=keyboard)


@dp.callback_query_handler(text='pass')
async def button_pass(query: types.CallbackQuery):
    global current_product_index
    current_product_index += 1
    await query.answer()
    await show_products(query.message)


@dp.callback_query_handler(text='start_over')
async def button_start_over(query: types.CallbackQuery):
    global current_product_index
    current_product_index = 0
    await query.answer()
    await show_products(query.message)


@dp.callback_query_handler(text='restart')
async def button_restart(query: types.CallbackQuery):
    global current_product_index
    current_product_index = 0
    await query.answer()
    await start(query.message)


# Unknown command handler
@dp.message_handler()
async def unknown_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Restart", callback_data='restart', alpha=0.7))

    await message.answer("I couldn't understand you.", reply_markup=keyboard)


def main():
    # Start the Bot
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
