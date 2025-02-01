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




@dp.message(lambda message: message.text == "📝 Oddiy test")
async def oddiy_test(message: types.Message, state: FSMContext):
    await message.answer(
        "✍️ Test javoblarini yuboring.\nM-n: abcdabcd \n ❕ Javoblar faqat lotin alifbosida bo'lishi shart."
    )
    await state.set_state(Oddiy_testState.answers)

import random

@dp.message(Oddiy_testState.answers)
async def oddiy_test_state_handler(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        telegram_id = message.from_user.id
        user  = message.from_user.username# Check if input contains only alphabetic characters
        answers = message.text  # Extract the text input
        count_answers = len(answers)
        code = ''.join(random.choices("123456789", k=4))
        # Create the test using the provided answers
        create_test(name="test",code = int(code), answers=answers, type="oddiy test", count=count_answers, telegram_id=telegram_id)

        # Clear the state after successful input processing
        await state.clear()
        await message.answer(f"✏️Nomi : Test \n📔Test kodi : {code} \n🔑Javoblari : {answers} \n🧮 soni:{count_answers} \n👨‍💼 Test yaratuvchi: @{user}\n\n ✅✅✅✅" )
        await message.answer("✅✅✅✅ Test muvaffaqiyatli Yaratildi!", reply_markup=test_yaratish())
    else:
        # If the input format is incorrect
        await message.answer(
            "Test yuborishda noto`g`ri formatdan foydalandingiz!",
            reply_markup=test_yaratish()
        )


@dp.message(lambda message: message.text == "♻️ Orqaga")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    # Reset the state (optional depending on your use case)
    await state.clear()

    # Send the main menu
    await message.answer(
        "Bosh menyu:",
        reply_markup=main_menu_buttons()  # Return the main menu buttons
    )


