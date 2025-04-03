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



@dp.message(lambda message: message.text == "✍️ Test yaratish")
async def admin_click(message: types.Message):
    await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup= test_yaratish())

@dp.message(lambda message: message.text == "📘 Qo'llanma")
async def sendqullanma(message: types.Message):
    
    await message.answer_video(
        video="BAACAgIAAxkBAAI94WfuTglxIh24tMrwoPw1OfMjR46AAAIHYwACooN4S7LhFx4K8UK-NgQ",  # Sending using the video ID
        caption="Bu yerda Qanday qilib TEST Yaratish  haqida ma'lumotlar mavjud.\n\n",
        
        parse_mode="HTML"  # Optional: Use Markdown or HTML for formatting
    )
    await message.answer_video(
        video="BAACAgIAAxkBAAI94GfuTgliN39JjMvJzTEDfcjyx54dAAIGYwACooN4S7iMywgcchnONgQ",  # Sending using the video ID
        caption="Bu yerda Qanday qilib TEST ISHLASH  haqida ma'lumotlar mavjud.\n\n"
        "❕ Test ishlash uchun videoni ko`ring:\n",
        parse_mode="HTML"  # Optional: Use Markdown or HTML for formatting
    )
