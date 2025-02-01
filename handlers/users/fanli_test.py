from aiogram.types import InlineKeyboardMarkup
from loader import dp,bot
from aiogram import types,F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from utils.misc.subscription import check
from middlewares.mymiddleware import CheckSubscriptionCallback
from api import *
from states.mystate import *
from aiogram.fsm.context import FSMContext
from keyboards.default.buttons import *
from aiogram.fsm.state import State, StatesGroup


@dp.message(lambda message: message.text == "📕 Fanli test")
async def oddiy_test(message: types.Message, state: FSMContext):
    # Ask for the name of the test
    await message.answer("📖 Fan nomini kiriting !!!")
    await state.set_state(FanliTestState.name)


@dp.message(FanliTestState.name)
async def oddiy_test_name_handler(message: types.Message, state: FSMContext):
    # Store the name in the state
    test_name = message.text
    await state.update_data(test_name=test_name)  # Save name in state

    await message.answer(
        "✍️ Test javoblarini yuboring.\nM-n: abcdabcd \n ❕ Javoblar faqat lotin alifbosida bo'lishi shart."
    )
    await state.set_state(FanliTestState.answers)


import random


@dp.message(FanliTestState.answers)
async def oddiy_test_state_handler(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        telegram_id = message.from_user.id
        user = message.from_user.username  # Get the username of the user
        answers = message.text  # Extract the text input
        count_answers = len(answers)
        code = ''.join(random.choices("123456789", k=4))

        # Retrieve the test name from the state
        user_data = await state.get_data()
        test_name = user_data.get('test_name')  # Get the name from the state

        # Create the test using the provided answers
        create_test(name=test_name, code=int(code), answers=answers, type="fanli test", count=count_answers,
                    telegram_id=telegram_id)

        # Clear the state after successful input processing
        await state.clear()

        # Send the response
        await message.answer(
            f"✏️ Nomi: {test_name} \n📔 Test kodi: {code} \n🔑 Javoblari: {answers} \n🧮 Soni: {count_answers} \n👨‍💼 Test yaratuvchi: @{user}\n\n ✅✅✅✅")
        await message.answer("✅✅✅✅ Test muvaffaqiyatli yaratildi!", reply_markup=test_yaratish())
    else:
        # If the input format is incorrect
        await message.answer("Test yuborishda notog'ri formatdan foydalandingiz!", reply_markup=test_yaratish())