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



@dp.message(lambda message: message.text == "✅ Javobni tekshirish")
async def checktest(message: types.Message, state: FSMContext):
    await message.answer("Test kodini yuboring !!!\n✅ Kod faqat raqamlardan iborat bo`lishi va 4 xonali bo`lishi kerak", reply_markup=orqaga())
    await state.set_state(check_oddiy_testState.code)


@dp.message(check_oddiy_testState.code)
async def check_code(message: types.Message, state: FSMContext):
    if message.text.isnumeric() and len(message.text) == 4:
        code = message.text  # Extract the code from the message
        try:
            # Fetch the test by code using the API
            test = get_test_by_code(code=code)

            # Validate the response
            if not isinstance(test, dict) or 'count' not in test or 'name' not in test or 'type' not in test:
                await message.answer("❌ Siz yuborgan kod bo'yicha birorta test topilmadi.",
                                     reply_markup=main_menu_buttons())
                return

            savollar_soni = test['count']
            name = test['name']
            type_test = test['type']

            # Retrieve the user's backend ID using their Telegram ID
            telegram_id = message.from_user.id
            user = get_user(telegram_id=telegram_id)
            if user == "Not Found":
                await message.answer("❌ Foydalanuvchi tizimda topilmadi. Iltimos, ro'yxatdan o'ting.")
                return

            backend_user_id = user['id']  # Get the backend user ID

            # Check if the user has already participated in the test
            existing_participation = get_test_participations(int(test['id']))
            if any(participation['user']['id'] == backend_user_id for participation in existing_participation):
                await message.answer("❌ Siz bu testda allaqachon ishtirok etgansiz.")
                return

            if test['status']==False:
                await message.answer("❌  bu test  allaqachon Tugagan")
                return
            # Save the test code to the state
            await state.update_data(code=code)

            # Inform the user about the test details
            await message.answer(
                f"✅ Test topildi\n"
                f"Nomi: {name}\n"
                f"Kod: {code}\n"
                f"Savollar soni: {savollar_soni}\n"
            )
            await message.answer(
                "✍️ Test javoblarini yuboring.\nM-n: abcdabcd \n❕ Javoblar faqat lotin alifbosida bo'lishi shart."
            )
            await state.set_state(check_oddiy_testState.answers)
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi: {str(e)}", reply_markup=main_menu_buttons())
    else:
        await message.answer("❌ Kod noto'g'ri. Iltimos, 4 xonali raqam yuboring.")


# Check the user's answers
@dp.message(check_oddiy_testState.answers)
async def check_answer(message: types.Message, state: FSMContext):
    # Ensure the message is valid
    if not message.text.isalpha():
        await message.answer("❌ Javoblar faqat lotin harflarida yuboring.")
        return

    user_answers = message.text.lower()  # Convert user input to lowercase
    code = (await state.get_data()).get('code')  # Get the test code from the state

    if not code:
        await message.answer("❌ Test Kodi noto`g`ri")
        return

    try:
        # Fetch the test by code using the API
        test = get_test_by_code(code=code)

        if isinstance(test, dict):  # Test found
            real_answers = test.get('answers', '').lower()  # Get real answers from the test
            if len(real_answers) != len(user_answers):
                await message.answer(
                    f"❌ Javoblar soni noto`g`ri .\nKutilgan javoblar soni {len(real_answers)} Lekin siz  {len(user_answers)}ta javob yubordiz."
                )
                return

            # Compare user answers with real answers
            correct = []
            incorrect = []
            for idx, (real, user) in enumerate(zip(real_answers, user_answers)):
                if real == user:
                    correct.append((idx + 1, user))
                else:
                    incorrect.append((idx + 1, user))

            # Calculate the correctness coefficient
            correct_count = len(correct)
            incorrect_count = len(incorrect)
            total_questions = len(real_answers)
            correctness_percentage = (correct_count / total_questions) * 100

            # Update TestParticipation model with the results
            user_id = message.from_user.id
            user_info = get_user(telegram_id=user_id)
            user_backend_id = user_info['id']

            test_id = test['id']
            answers_data = {
                'user_id': user_backend_id,
                'test_id': test_id,
                'correct_answer': correct_count,
                'wrong_answer': incorrect_count,
                'answers': user_answers,
                'certificate': True if correctness_percentage >= 80 else False
                     # Assuming 80% is required for certification
            }

            # Here you can call the create_test_participation function to save the results
            create_test_participation(
                user_id=answers_data['user_id'],
                test_id=answers_data['test_id'],
                answers=answers_data['answers'],
                correct_answer=answers_data['correct_answer'],
                wrong_answer=answers_data['wrong_answer'],
                certificate=answers_data['certificate'],
            )

            # Format and send the response
            result_message = (
                f"📋 Test natijalari:\n"
                f"👤 Foydalanuvchi: {message.from_user.full_name}\n"
                f"🔢 Savollar soni: {test['count']}\n\n"
                f"✅ To'g'ri javoblar: {correct_count}\n"
                f"❌ Noto'g'ri javoblar: {incorrect_count}\n\n"
                f"📈 To'g'ri ishlash ko'rsatkichi: {correctness_percentage:.2f}%\n\n"
                f"📝 Test tuzuvchisi: {test['owner']['first_name']} {test['owner']['last_name']}\n"
            )
            await message.answer(result_message, reply_markup=main_menu_buttons())
            await message.answer("bosh menu", reply_markup=main_menu_buttons())
        else:
            await message.answer("❌ Test topilmadi. Kodni qayta tekshiring.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")
