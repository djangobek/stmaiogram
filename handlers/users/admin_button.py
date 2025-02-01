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





@dp.message(lambda message: message.text == "👨‍⚕️ Admin")
async def admin_click(message: types.Message):
    await message.answer("👨‍⚕️ Admin: @Nurbekabdurashitov", reply_markup= main_menu_buttons())
