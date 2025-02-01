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
from openpyxl import Workbook
from io import BytesIO
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
# Assume this function queries your DB
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
import io
from fpdf import FPDF
from aiogram import types
from jinja2 import Template
from datetime import datetime
from io import BytesIO

# Define the callback data for each test (to handle button clicks)
test_callback = CallbackData()



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message(lambda message: message.text == "📂 mening testlarim")
async def view_user_tests(message: types.Message):
    # Fetch all tests for the user (owner == message.from_user.id)
    user_tests = get_tests_by_owner(message.from_user.id)

    if not user_tests:
        await message.answer("Sizning testlaringiz mavjud emas.")
        return

    # Create a list to store inline buttons
    inline_buttons = []

    # Add each test as a button
    for test in user_tests:
        if isinstance(test, dict):
            status_emoji = "✅" if test['status'] else "❌"
            test_code = test['code']

            # Directly construct callback data as a string
            callback_data = f"test:{test_code}"
            button = InlineKeyboardButton(
                text=f"{status_emoji} Test kodi: {test_code}",
                callback_data=callback_data
            )
            inline_buttons.append(button)
        else:
            print(f"Skipping invalid test: {test}")

    # Add the "Orqaga" button
    orqaga_button = InlineKeyboardButton(
        text="🔙 Orqaga",
        callback_data="back_to_main_menu"
    )
    inline_buttons.append(orqaga_button)

    # Create the inline keyboard
    row_width = 1
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[inline_buttons[i:i + row_width] for i in range(0, len(inline_buttons), row_width)]
    )

    # Send the message with the inline keyboard
    await message.answer("Sizning testlaringiz:", reply_markup=keyboard)

# Handle the test button click
# @dp.callback_query(test_callback.filter())
# async def handle_test_click(callback_query: types.CallbackQuery, callback_data: dict):
#     test_code = callback_data["test_code"]
#
#     # Fetch the test details by the test code
#     test_details = get_test_by_code(test_code)
#
#     if not test_details:
#         await callback_query.answer("Test topilmadi.")
#         return
#
#     # Format the message with test details
#     status_emoji = "✅" if test_details['status'] else "❌"
#     response = (
#         f"📚 Test kodi: {test_details['code']}\n"
#         f"📖 Test nomi: {test_details['name']}\n"
#         f"🔑 Javoblar: {test_details['answers']}\n"
#         f"🧮 Soni: {len(test_details['answers'])}\n"
#         f"Status: {status_emoji}\n"
#     )
#
#     # Send the test details to the user
#     await callback_query.message.answer(response)
#
#     # Optionally, send a success reply to the user
#     await callback_query.answer("Test tafsilotlari ko'rsatilmoqda.")

# Callback handler for test details
@dp.callback_query(lambda query: query.data.startswith("test:"))
async def handle_test_callback(query: types.CallbackQuery):
    # Extract the test code from the callback data
    test_code = query.data.split(":")[1]

    # Fetch test details using the `get_test_by_code` function
    test_details = get_test_by_code(test_code)

    if "error" in test_details:
        await query.message.answer(f"Test topilmadi yoki xato yuz berdi: {test_details['error']}")
        return

    # Extract details from the response
    test_name = test_details.get("name", "Noma'lum")
    test_id = test_details.get("id")  # Assuming `id` is part of the test details
    test_status = "✅ Faol" if test_details.get("status") else "❌ Faol emas"

    # Fetch participation data
    participations = get_test_participations(test_id)
    participant_count = len(participations)

    # Count valid and invalid certificates
    certificate_true_count = sum(1 for p in participations if p.get("certificate") is True)
    certificate_false_count = participant_count - certificate_true_count

    # Construct the message
    message_text = (
        f"📝 Test nomi: {test_name}\n"
        f"👥 Ishtirokchilar soni: {participant_count}\n"
        f"✅ Sertifikat Olganlar: {certificate_true_count}\n"
        f"❌ Sertifikat Ololmaganlar: {certificate_false_count}\n"
        f"📌 Status: {test_status}\n"
    )

    # Create inline buttons
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔴 Yakunlash",
                    callback_data=f"finish:{test_code}"
                ) if test_details.get("status") else InlineKeyboardButton(
                    text="🟢 Qayta ishga tushurish",
                    callback_data=f"restart:{test_code}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📄 Data PDF",
                    callback_data=f"pdf:{test_code}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data="back_to_tests"
                )
            ]
        ]
    )

    # Send the message with the test details and inline buttons
    await query.message.edit_text(message_text, reply_markup=keyboard)

@dp.callback_query(lambda query: query.data == "back_to_tests")
async def back_to_tests_callback(query: types.CallbackQuery):
    await query.message.edit_text("📂 Sizning testlaringiz:", reply_markup=await generate_user_tests_keyboard(query.from_user.id))


async def generate_user_tests_keyboard(user_id: int):
    """
    Generate the inline keyboard for the user's tests.
    """
    user_tests = get_tests_by_owner(user_id)

    if not user_tests:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Hech qanday test mavjud emas", callback_data="no_tests")]
        ])

    inline_buttons = [
        InlineKeyboardButton(
            text=f"✅ Test kodi: {test['code']}" if test["status"] else f"❌ Test kodi: {test['code']}",
            callback_data=f"test:{test['code']}"
        )
        for test in user_tests
    ]
    orqaga_button = InlineKeyboardButton(
        text="🔙 Orqaga",
        callback_data="back_to_main_menu"
    )
    inline_buttons.append(orqaga_button)

    row_width = 1
    return InlineKeyboardMarkup(
        inline_keyboard=[inline_buttons[i:i + row_width] for i in range(0, len(inline_buttons), row_width)]
    )
# Handlers for "Qayta ishga tushurish" and "Yakunlash"
@dp.callback_query(lambda query: query.data.startswith("restart:") or query.data.startswith("finish:"))
async def handle_test_status_change(query: types.CallbackQuery):
    action, test_code = query.data.split(":")
    test_details = get_test_by_code(test_code)
    if "error" in test_details:
        await query.message.answer(f"Test kodi '{test_code}' bo'yicha ma'lumot topilmadi.")
        return

    test_id = test_details.get("id")

    if not test_id:
        await query.message.answer(f"Test kodi '{test_code}' bo'yicha ma'lumot topilmadi.")
        return

    if action == "restart":
        update_test_status_api(test_id=test_id)
        # Restart the test logic here
        await query.answer(f"Test {test_code} qayta ishga tushirildi!")
    elif action == "finish":
        # Finish the test logic here
        update_test_status_api(test_id=test_id)
        await query.answer(f"Test {test_code} yakunlandi!")

# Handler for "Data PDF"
@dp.callback_query(lambda query: query.data.startswith("pdf:"))
async def send_test_participation_html(query: types.CallbackQuery):
    test_code = query.data.split(":")[1]
    await query.message.answer("Test hisobotini tayyorlash boshlandi...")

    test_details = get_test_by_code(test_code)
    if "error" in test_details:
        await query.message.answer(f"Test kodi '{test_code}' bo'yicha ma'lumot topilmadi.")
        return

    test_id = test_details.get("id")
    total_questions = test_details.get("count", 0)
    test_quality = test_details.get("quality", "Noma'lum")

    participations = get_test_participations(test_id)

    if not participations:
        await query.message.answer("Ushbu test uchun ishtirokchilar topilmadi.")
        return

    sorted_participations = sorted(
        participations,
        key=lambda x: (-int(x.get("correct_answer", 0)), x.get("participated_at", "9999-12-31T23:59:59")),
    )

    def format_test_time(test_time):
        try:
            dt = datetime.fromisoformat(test_time[:-6])  # Remove timezone offset
            return dt.strftime("%d.%m.%Y %H:%M:%S")  # Format as 30.01.2025 14:00:59
        except ValueError:
            return "Noma'lum"

    # Extract correct answers safely
    correct_answers_dict = {}
    if test_details.get("answers"):
        correct_answers_dict = {
            str(i + 1): answer  # Convert to question number (1,2,3...)
            for i, answer in enumerate(test_details["answers"])
        }

    print("Extracted correct answers:", correct_answers_dict)  # Debugging

    for index, participant in enumerate(sorted_participations, start=1):
        user = participant.get("user", {})
        fullname = user.get("name") or f"{user.get('first_name', 'Noma\'lum')} {user.get('last_name', '').strip()}"

        user_answers = list(participant.get("answers", ""))  # Convert to list of letters

        correct_answers = []
        wrong_answers = []
        correcto = participant.get("correct_answer", "")
        wrongo = participant.get("wrong_answer", "")
        user_time = format_test_time(participant.get("participated_at", 0))
        total_questions = participant.get("answers", "")

        if len(total_questions) > 0:
            performance = round((int(correcto) / len(total_questions)) * 100, 2)
        else:
            performance = 0

        def calculate_test_quality(participations, total_questions):
            """
            Calculates test quality based on the number of correct answers.

            :param participations: List of participants with correct answers.
            :param total_questions: Total number of questions in the test.
            :return: Test quality percentage (0-100)
            """
            if not participations or total_questions == 0:
                return 0  # Avoid division by zero

            total_correct_answers = sum(int(p.get("correct_answer", 0)) for p in participations)
            total_possible_answers = total_questions * len(participations)

            return round((total_correct_answers / total_possible_answers) * 100, 2) if total_possible_answers else 0

        test_quality = calculate_test_quality(sorted_participations, len(test_details.get("answers")))

        for question_number, user_answer in enumerate(user_answers, start=1):
            correct_answer = correct_answers_dict.get(str(question_number), "Noma'lum")

            if user_answer == correct_answer:
                correct_answers.append(f"{question_number}-{correct_answer}")
            else:
                wrong_answers.append(f"{question_number}-{correct_answer}({user_answer})")

        participant["rank"] = index
        participant["fullname"] = fullname
        participant["correct_count"] = correcto
        participant["wrong_count"] = wrongo
        participant["user_time"] = user_time
        participant["wrong_details"] = ", ".join(wrong_answers)
        participant["test_quality"] = test_quality
        participant["performance"] = f"{performance}%"
    template_html = """
    <html>
<head>
    <title>Test Hisoboti</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }
        .container { width: 80%; margin: auto; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid black; padding: 10px; text-align: center; }
        th { background-color: #007BFF; color: white; }
        .header { text-align: center; margin-bottom: 20px; }
        .highlight { font-weight: bold; color: #28a745; font-size: 18px; }
        .red-text { color: red; }
        .test-quality { font-size: 18px; font-weight: bold; padding: 5px 10px; border-radius: 5px; display: inline-block; }
        .good-quality { background-color: #28a745; color: white; }
        .medium-quality { background-color: #ffc107; color: black; }
        .low-quality { background-color: #dc3545; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Test kodi: {{ test_code }}</h2>
            <p><span class="highlight">Savollar soni:</span> {{ total_questions }} ta</p>
            <p><span class="highlight">Testda qatnashganlar soni:</span> {{ total_participants }} ta</p>
            <p>
            
                
            </p>
        </div>
        <table>
            <tr>
                <th>Nechanchi o'rin</th>
                <th>F.I.O.</th>
                <th>To'g'ri javoblar soni</th>
                <th>Noto'g'ri javoblar soni</th>
                <th>Test topshirgan vaqti</th>
                <th class="red-text">Noto'g'ri javoblar</th>
                <th>Ishlash ko‘rsatkichi (%)</th>
            </tr>
            {% for p in participants %}
            <tr>
                <td>{{ p.rank }}</td>
                <td>{{ p.fullname }}</td>
                <td>{{ p.correct_count }}</td>
                <td>{{ p.wrong_count }}</td>
                <td>{{ p.user_time }}</td>
                <td class="red-text">{{ p.wrong_details }}</td>
                <td>{{ p.performance }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>

    """

    template = Template(template_html)
    rendered_html = template.render(
        test_code=test_code,
        total_questions=total_questions,
        total_participants=len(participations),
        test_quality=test_quality,
        participants=sorted_participations,
    )

    html_file = BytesIO(rendered_html.encode("utf-8"))
    html_file.seek(0)

    await query.message.answer_document(
        document=types.BufferedInputFile(html_file.read(), filename=f"test_{test_code}_report.html"),
        caption="Test ishtirokchilari haqida ma'lumot.",
        reply_markup=main_menu_buttons()
    )
    await query.message.answer("Hisobot tayyor!")

@dp.callback_query(lambda query: query.data == "back_to_main_menu")
async def back_to_main_menu(query: types.CallbackQuery):
    keyboard = main_menu_buttons()  # Ensure this returns a ReplyKeyboardMarkup

    # Delete the inline message and send a new one
    await query.message.delete()
    await query.message.answer(
        text="Bosh menyu",
        reply_markup=keyboard  # Correctly pass the ReplyKeyboardMarkup
    )

