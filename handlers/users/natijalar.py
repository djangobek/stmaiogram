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



@dp.message(lambda message: message.text == "🏆 Natijalar")
async def send_results(message: types.Message):
    file_ids = get_files() # Debugging line

    if not file_ids:
        await message.answer("Hozircha hech qanday fayl mavjud emas.")
        return

    await message.answer("Sardor Uteganovning 2024-yildagi barcha natijalari")
    for file_id in file_ids:
        try:
            await bot.send_document(chat_id=message.chat.id, document=file_id)
        except Exception as e:
            print(f"Failed to send file {file_id}: {e}")  # Debugging


@dp.message(lambda message: message.document)
async def handle_document(message: types.Message):
    """
    When a user sends a document, the bot sends back the file_id.
    """
    file_id = message.document.file_id

    # Send file_id back as a code block
    await message.answer(f"{file_id}",)