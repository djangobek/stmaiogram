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
    file_ids = ["BQACAgIAAxkBAAILx2exnU0tvcnsVllliuXSs7I4L56eAAJiVgACYisZStaQpQZZxDfANgQ", "BQACAgIAAxkBAAILzGexnU0SoxxYrUzJSLdO-JSw1Qi9AAKSVwAC7iAoSuAC_GJUqS7HNgQ", "BQACAgIAAxkBAAIL0GexnU0oT6BocJ9PjGkzEJ68IAn0AAJ6WAAC7iAoSjQXvdyxzCAZNgQ", "BQACAgIAAxkBAAILyGexnU1WEuQcFrIrtFr3CWCHucR8AAKOVwAC7iAoSrMQeAQwWFm2NgQ", "BQACAgIAAxkBAAILy2exnU1FYbkraQftOahuA-XMDmSZAAKRVwAC7iAoSumBAagqeaY5NgQ", "BQACAgIAAxkBAAILyWexnU1iY42qTNcaQzXK9jqfxJNqAAKPVwAC7iAoSqFVHT7TjCVqNgQ", "BQACAgIAAxkBAAILymexnU1VMMi2RuFob8qU4fgV99R5AAKQVwAC7iAoSnUMhKiyG4GANgQ", "BQACAgIAAxkBAAILzmexnU3yNSjz3C5yn8YSbCNTSp5XAAKUVwAC7iAoSvedp5c_v9VdNgQ", "BQACAgIAAxkBAAILz2exnU0Lc9Y02tsIdcuGRF9vZziIAAKVVwAC7iAoSk48kUtH0AOBNgQ", "BQACAgIAAxkBAAIL0mexnU1Qt7D3_8H4mlTGcdi7NzXYAAJ8WAAC7iAoSr_K6qobgvhTNgQ", "BQACAgIAAxkBAAIL5WexnU3pAVU1ec1xrSmgGhqiDjhIAAI1WgAC7iAoSuu6rY86ilSxNgQ", "BQACAgIAAxkBAAIL5mexnU2jwgli-DlkP6kT8MFZGNQpAAI2WgAC7iAoSo4AAd6R0uRiqDYE", "BQACAgIAAxkBAAIL7mexnU3JDrmcRrq85Dy5MsH6mRVvAAKIWwAC7iAoSuVzQLUSaxgsNgQ", "BQACAgIAAxkBAAIL6GexnU1u4-7WGb4nl5B1BhYYgKmGAAIkWwAC7iAoSvZM82kQLrfbNgQ", "BQACAgIAAxkBAAIL7WexnU01Mib_9ZfzvKykYeeCAx45AAJNWwAC7iAoSn-TFAXPmL6hNgQ", "BQACAgIAAxkBAAIL42exnU2HLy7Sa7DKURcPW3rf3ehnAAIzWgAC7iAoSkWBKSwDqMKgNgQ", "BQACAgIAAxkBAAIL4WexnU33524sPwm49KnOU3YJyRH0AAIxWgAC7iAoStGG4PaO9Yw3NgQ", "BQACAgIAAxkBAAIL9WexnU1Pw_t8wBMwkJhffAb1Tp2jAALXWwAC7iAoSm8Elq30h-91NgQ", "BQACAgIAAxkBAAIL6WexnU13diEQMzc08POl2kzgw9z3AAIlWwAC7iAoShx4VsgNCPqzNgQ", "BQACAgIAAxkBAAIL8WexnU3pdLlOCvYqx0DSA5T7C7XSAAKNWwAC7iAoSmski3tTDjddNgQ", "BQACAgIAAxkBAAIL4GexnU2fJu0ZngMXUN6_qCeeOa4FAAIwWgAC7iAoSj2f1FESziNkNgQ", "BQACAgIAAxkBAAIL82exnU1CAAHj_jujlpGP9huqj5H8FQAC1VsAAu4gKEo285r067oeiTYE", "BQACAgIAAxkBAAIL02exnU3B92wvRZ6QjrCxRvoBKgbuAAJ9WAAC7iAoSk_KWYqgNYIrNgQ", "BQACAgIAAxkBAAIL1GexnU3gnVMcGTn168WPxYoXrAq1AAJ-WAAC7iAoSuA5HYpZxVRDNgQ", "BQACAgIAAxkBAAIL92exnU302dl-F1tx_SjyvaLnwou2AAIwXAAC7iAoSt6gshQ137MDNgQ", "BQACAgIAAxkBAAIL-WexnU0AAat1Kz86qoma2jf3tyr3GAAC9VQAAkQ7UUp6Wd6kNrQe2jYE", "BQACAgIAAxkBAAIL32exnU0oN897Z1NBxIfsbDj3n71AAAIvWgAC7iAoSqDrokjue_VrNgQ", "BQACAgIAAxkBAAIL-GexnU0j8OmAWGEBZ3D0vzuZ18xXAAIxXAAC7iAoSvyXrzJbFUjRNgQ", "BQACAgIAAxkBAAIL5GexnU1oPWRPKvgY5J_dsDtIlzLmAAI0WgAC7iAoSm1A8J9uJYT8NgQ", "BQACAgIAAxkBAAIL9GexnU2UrqjUMUTUa5pPRfyciXrPAALWWwAC7iAoSoLu3m2f0vW9NgQ", "BQACAgIAAxkBAAIL72exnU0YVS6kcrZTi1lBduD__U-IAAKLWwAC7iAoSsgYdqyk5ZuhNgQ", "BQACAgIAAxkBAAIL9mexnU2xLj3L5I3fm0ASHGbb4hMTAAILXAAC7iAoSmeQPHPkNM9wNgQ", "BQACAgIAAxkBAAIL0WexnU1cQVtuXtqzRMOkFoeWJNdgAAJ7WAAC7iAoSosY8_IcIOt0NgQ", "BQACAgIAAxkBAAIL-mexnU1g8HGlT6ijHfJOUdgaWCeKAAITUAAClMRgSr5W421VeSdDNgQ", "BQACAgIAAxkBAAIL3WexnU04l3-qZrs-yYHdx0GPcUvfAAItWgAC7iAoSjuCkYMYyX3DNgQ", "BQACAgIAAxkBAAILzWexnU1iFCTSNbF4Khc2acguwvC-AAKTVwAC7iAoSrI5sU0pzNyjNgQ", "BQACAgIAAxkBAAIL-2exnU3GTIyav-FasSS8o2wavJ51AAL3ZwACrvPBS7zU87yxSIkrNgQ", "BQACAgIAAxkBAAIL1mexnU2ov503sYVbiDNiyIfiuFeiAAKBWAAC7iAoSvE6p9IQB1byNgQ", "BQACAgIAAxkBAAIL2WexnU3yrXsNVDX5WgkOZp2jVCVWAAIrWQAC7iAoSh6XUzYilSVZNgQ", "BQACAgIAAxkBAAIL3GexnU2HmUEMHacQ7o3vFpH2iN0DAAIsWgAC7iAoSjM5TUiucKtINgQ", "BQACAgIAAxkBAAIL12exnU25EQidqySOP5HFfP6rzuQWAAIpWQAC7iAoSk1kai6gmOI9NgQ", "BQACAgIAAxkBAAIL22exnU359r9IOB7UisDL3MXe6Rv6AAJoWQAC7iAoSnfOxPZixc3INgQ", "BQACAgIAAxkBAAIL2mexnU2W7kzA6WZA3xqeOROnM3tYAAJmWQAC7iAoSrFg4twmG86INgQ", "BQACAgIAAxkBAAIL8mexnU0dTSZlm3YQzG-rtlMNDSWYAAKOWwAC7iAoSsrhLlNtLl57NgQ", "BQACAgIAAxkBAAIL2GexnU2PtsHo1I8y4LpB7GpURgRtAAIqWQAC7iAoSsS7UhHZqIJeNgQ", "BQACAgIAAxkBAAIL4mexnU0eWJFSmyVUsZJh34sokiSxAAIyWgAC7iAoSrNm0ih316ERNgQ", "BQACAgIAAxkBAAIL7GexnU2tg9A95Z_0jI5n9l1fMEWXAAIqWwAC7iAoSv-lBCazmUuwNgQ", "BQACAgIAAxkBAAIL62exnU2FNEyAxcclq5OUZ_eb_8q2AAIpWwAC7iAoSpzzMkiutIqxNgQ", "BQACAgIAAxkBAAIL3mexnU1l8pD6CMd5z5n2PCC-3OvcAAIuWgAC7iAoSgABKKpFLKBfrjYE", "BQACAgIAAxkBAAIL52exnU1TZGfjfOk7dTGg-g4kyeElAAIjWwAC7iAoSiQAAQGLVr4p4TYE", "BQACAgIAAxkBAAIL6mexnU1TLlU-HFwHl6UX1CrUI22rAAInWwAC7iAoSij66sO3D-JqNgQ", "BQACAgIAAxkBAAIL8GexnU0u46nC-xcNjFY-hKSHELZmAAKMWwAC7iAoSpala5ZQHermNgQ", "BQACAgIAAxkBAAIL1WexnU0ObS3mI0X7d5UCDyRnpj_yAAJ_WAAC7iAoSjc3xlawGqMCNgQ"] # Debugging line

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