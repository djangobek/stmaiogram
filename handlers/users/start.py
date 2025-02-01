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
import os
start_text_uz = '''
✍️ Ismingiz va familiyangizni kiriting.\n\n
❗️ Ism va familiya faqat lotin alifbosida bo'lishi shart.
'''
start_text_en = '''
✍️ Enter your first name and last name.\n\n
❗️ Name and surname must be in Latin alphabet only.
'''
subs = '''
Iltimos, bot to'liq ishlashi uchun quyidagi kanallarga obuna bo'ling!
'''

@dp.message(CommandStart())
async def start_chat(message: types.Message, state: FSMContext):
    user = get_user(telegram_id=message.from_user.id)
    language = user.get('language', 'uz') if user != 'Not Found' else 'uz'

    try:
        create_user(name=message.from_user.full_name, telegram_id=message.from_user.id)
    except Exception as e:
        print(f"Error creating user: {e}")

    btn = InlineKeyboardBuilder()
    final_status = True
    channels = get_all_channels()
    if channels:
        for channel in channels:
            status = True
            try:
                status = await check(user_id=message.from_user.id, channel=channel['channel_id'])
            except Exception as e:
                print(f"Error checking subscription: {e}")
                pass
            final_status *= status
            if not status:
                try:
                    channel = await bot.get_chat(channel['channel_id'])
                    invite_link = await channel.export_invite_link()
                    btn.row(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
                except Exception as e:
                    print(f"Error fetching channel: {e}")

        btn.button(text='Obunani tekshirish', callback_data=CheckSubscriptionCallback(check=True))
        btn.adjust(1)
        if not final_status:
            await message.answer(text=subs, reply_markup=btn.as_markup(row_width=1))
            return

    await message.answer(text=start_text_uz if language == 'uz' else start_text_en)
    await state.set_state(Namesurname.full_name)

@dp.message(Namesurname.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    # Split the user's input into first name and last name
    full_name = message.text.strip()
    name_parts = full_name.split(maxsplit=1)  # Split into two parts: first name and last name

    if len(name_parts) < 2:
        await message.answer("❗️ Iltimos, to'liq ismingiz va familiyangizni kiriting (masalan: Ali Valiyev).")
        return

    first_name, last_name = name_parts
    await state.update_data(first_name=first_name, last_name=last_name)

    # Save the user details
    update_user_details(telegram_id=message.from_user.id, first_name=first_name, last_name=last_name)

    # Greet the user and finish the state
    await message.answer(f'Assalomu alaykum {first_name} {last_name}, botimizga xush kelibsiz.', reply_markup=main_menu_buttons())
    await state.clear()
@dp.callback_query(CheckSubscriptionCallback.filter())
async def test(call:types.CallbackQuery):
    await call.answer(cache_time=60)
    user = get_user(telegram_id=call.from_user.id)
    if user != 'Not Found':
        language = user.get('language', 'uz')
    else:
        language = 'uz'
    k = []
    final_status = False
    user_id = call.from_user.id
    kanallar = get_all_channels()
    for kanal in kanallar:
        try:
            channel = await bot.get_chat(kanal['channel_id'])
        except:
            pass
        try:
            res = await bot.get_chat_member(chat_id=kanal['channel_id'], user_id=user_id)
        except:
            continue
        if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
            k.append(InlineKeyboardButton(text=f"✅ {channel.title}", url=f"{await channel.export_invite_link()}"))

        else:
            k.append(InlineKeyboardButton(text=f"❌ {channel.title}", url=f"{await channel.export_invite_link()}"))
            final_status = True
    builder = InlineKeyboardBuilder()
    builder.add(*k)
    builder.button(text='Obunani tekshirish', callback_data=CheckSubscriptionCallback(check=True))
    builder.adjust(1)
    if final_status:
        await bot.send_message(chat_id=user_id,
                               text=subs,
                               reply_markup=builder.as_markup())
    else:
        await call.message.answer(start_text_en if language=='en' else start_text_uz)
    await call.message.delete()





