from aiogram.utils.keyboard import ReplyKeyboardBuilder,KeyboardButton
def admin_button():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="🗣 Reklama yuborish"),
        KeyboardButton(text="📊 Obunachilar soni"),

    )
    button.row(KeyboardButton(text="🗣 Kanal qo'shish"),
               KeyboardButton(text="🗣 Kanallar"))
    button.adjust(2,2)
    return button.as_markup(resize_keyboard=True,one_time_keyboard=True,input_field_placeholder="Kerakli bo'limni tanlang!")
def add_type():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="📝 Tekst"),
        KeyboardButton(text="📸 Rasm")
    )
    button.row(
        KeyboardButton(text="🎞 Video"),
        KeyboardButton(text="⬅️ Orqaga")
    )
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)
def back_button():
    button = ReplyKeyboardBuilder()

    button.row(

        KeyboardButton(text="◀️ Orqaga")
    )
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)
def need_or_not():
    button = ReplyKeyboardBuilder()

    button.row(
        KeyboardButton(text="⏺ Bekor qilish"),
        KeyboardButton(text="🆗 Kerakmas")
    )
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)
def send():
    button = ReplyKeyboardBuilder()

    button.row(
        KeyboardButton(text="⏺ Bekor qilish"),
        KeyboardButton(text="📤 Yuborish")
    )
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)


def main_menu_buttons():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="✍️ Test yaratish"),
        KeyboardButton(text="✅ Javobni tekshirish"),
    )
    button.row(
        KeyboardButton(text="📂 mening testlarim"),
    )
    button.row(
        KeyboardButton(text="📘 Qo'llanma"),
        KeyboardButton(text="👨‍⚕️ Admin"),
    )
    button.adjust(2)  # Adjust the layout to 2 buttons per row
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)

def test_yaratish():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="📝 Oddiy test"),
    )
    button.row(
        KeyboardButton(text="📕 Fanli test"),
    )
    button.row(
        KeyboardButton(text="♻️ Orqaga"),
    )
    button.adjust(2)  # Adjust the layout to 2 buttons per row
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)


def orqaga():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="♻️ Orqaga")
    )
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)
