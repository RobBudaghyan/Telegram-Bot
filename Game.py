import aiogram

bot_token = '6149138821:AAHGpgxw2JUpVMkrvKQ8JvM0923YqnWBh1Y'  # Replace with your bot token

bot = aiogram.Bot(token=bot_token)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def handle_start(message: aiogram.types.Message):
    keyboard_markup = aiogram.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    choice_buttons = [aiogram.types.KeyboardButton(str(i)) for i in range(1, 5)]
    keyboard_markup.add(*choice_buttons)

    await message.answer("Welcome! Click on a number:", reply_markup=keyboard_markup)


@dp.message_handler(content_types=['text'])
async def handle_choice(message: aiogram.types.Message):
    choice = message.text

    if choice in ('1', '2', '3', '4'):
        number = {
            '1': 'One',
            '2': 'Two',
            '3': 'Three',
            '4': 'Four'
        }.get(choice)

        await message.answer(number)
    else:
        await message.answer("Invalid choice. Please select a number from 1 to 4.")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
