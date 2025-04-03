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
    caption_text = (
        "📚 *Test Ishlash va Javoblarni Tekshirish Boti* 🤖\n\n"
        "Assalomu alaykum! 🎯\n"
        "Yangi bot orqali test ishlash va javoblaringizni tekshirish imkoniyati! 🚀\n\n"
        "✅ *Botning imkoniyatlari:*\n"
        "- Test savollarini yechish ✍️\n"
        "- Javoblaringizni avtomatik tekshirish ✅\n"
        "- To'g'ri va noto'g'ri javoblaringizni ko'rsatish 📊\n\n"
        "📌 *Qanday ishlatish kerak?*\n"
        "1. Botga /start buyrug'ini yuboring.\n"
        "2. Test savollarini oling va javoblaringizni yozing.\n"
        "3. Javoblaringizni botga yuboring va natijalaringizni oling.\n\n"
        "📩 *Javoblarni tekshirish:*  \n"
        "Bot sizning javoblaringizni avtomatik tekshiradi, to'g'ri va noto'g'ri javoblaringizni ko'rsatadi. 📝\n\n"
        "📊 *Natijalaringizni bilish:*  \n"
        "Har bir test yakunida to'liq statistikangizni olishingiz mumkin. 📈\n\n"
        "👉 *Boshlash uchun:* [/start](/start)\n\n"
        "ℹ️ *Qo'shimcha ma'lumot:*  \n"
        "Agar savollaringiz bo'lsa, botga yozing yoki biz bilan bog'laning. \n"
        "@zohidxon_rasaxonov"
    )
    await message.answer_video(
        video="BAACAgIAAxkBAAI94WfuTglxIh24tMrwoPw1OfMjR46AAAIHYwACooN4S7LhFx4K8UK-NgQ",  # Sending using the video ID
        caption=caption_text,
        
        parse_mode="HTML"  # Optional: Use Markdown or HTML for formatting
    )
    await message.answer_video(
        video="BAACAgIAAxkBAAI94GfuTgliN39JjMvJzTEDfcjyx54dAAIGYwACooN4S7iMywgcchnONgQ",  # Sending using the video ID
        caption="Bu yerda Qanday qilib TEST ISHLASH  haqida ma'lumotlar mavjud.\n\n"
        "❕ Test ishlash uchun videoni ko`ring:\n",
        parse_mode="HTML"  # Optional: Use Markdown or HTML for formatting
    )
    await message.answer_video(
        video="BAACAgIAAxkBAAI932fuTglSEMSvFwzVzc-XG8LHyaF7AAICYwACooN4S4mF8Cy9LESJNgQ",  # Sending using the video ID
        caption="Endi Siz botdan bemalol foydalana olasiz !.\n\n"
        "❕ Test ishlash uchun videoni ko`ring:\n",
        parse_mode="HTML"  # Optional: Use Markdown or HTML for formatting
    )
