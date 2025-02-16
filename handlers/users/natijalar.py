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
    file_ids = [
              "BQACAgIAAxkBAAIbkWex9twMs6FBMIsaNfB6HtYxdEcoAAJiVgACYisZStbqIJnlnGxkNgQ",
              "BQACAgIAAxkBAAIbmWex9tzScI_bXWryUH7DXWxpuTXBAAKVVwAC7iAoSnyuuDaG88lKNgQ",
              "BQACAgIAAxkBAAIbl2ex9twj9TFukiiSaTWTvhQBya5mAAKTVwAC7iAoSjtDH5rIAV9rNgQ",
              "BQACAgIAAxkBAAIbp2ex9twNyVhxQ9JTWMDHl-Ho09R1AAItWgAC7iAoSnWT84Czg8SnNgQ",
              "BQACAgIAAxkBAAIbn2ex9twehz2uo4_93Kwi6PNB6TCtAAJ_WAAC7iAoSpUfCUNxDWHxNgQ",
              "BQACAgIAAxkBAAIbm2ex9twr1zr-rrvIeJzeNv0g4BDCAAJ7WAAC7iAoSqDx0kNsIjPtNgQ",
              "BQACAgIAAxkBAAIbk2ex9tzcX0BBiwo9s-BUuX4TEX0VAAKPVwAC7iAoSpwx8TReuB38NgQ",
              "BQACAgIAAxkBAAIbpWex9tyZeeiwmVs46H3DtefCWcL_AAJoWQAC7iAoShAJIxCnfKxjNgQ",
              "BQACAgIAAxkBAAIboWex9txFhzTUt8YDtF35F6UDeAIPAAIpWQAC7iAoSkLNM4ayTUKoNgQ",
              "BQACAgIAAxkBAAIbnWex9tzLYVbBEDbn8vn-JZ6EAAHn6AACfVgAAu4gKEoX4nlcywJVOTYE",
              "BQACAgIAAxkBAAIbr2ex9txpNnhgvoszie9ryrUxBwgTAAI1WgAC7iAoSkQQxzmkpaOJNgQ",
              "BQACAgIAAxkBAAIbs2ex9tx8kfi1Kejf0d1H1SnIjlTZAAIlWwAC7iAoSpbqcL76lui8NgQ",
              "BQACAgIAAxkBAAIbq2ex9txg3PksaFzmkocgS4TDcAlVAAIxWgAC7iAoSrgiPXsHKHxyNgQ",
              "BQACAgIAAxkBAAIbtWex9txfTvfzs6now52jEsvJejCNAAIpWwAC7iAoSktuLyLUe9poNgQ",
              "BQACAgIAAxkBAAIbqWex9twFW5lWPLvqhGrEaeKmX4wsAAIvWgAC7iAoSrT8ott-VNkXNgQ",
              "BQACAgIAAxkBAAIbo2ex9twcgSwFM3YE5CByPJJltjBHAAIrWQAC7iAoSvhbuLvmUBXaNgQ",
              "BQACAgIAAxkBAAIbsWex9ty26glbOIt4_PRI1IxD4Qb2AAIjWwAC7iAoSnCSFoF9SEiNNgQ",
              "BQACAgIAAxkBAAIbvWex9txlMKV5pjgpGpmwMmPqKSxXAALVWwAC7iAoSnxnDvd82OfWNgQ",
              "BQACAgIAAxkBAAIblWex9tyevzXxH5neCnfb2taWu1P-AAKRVwAC7iAoShtnZ0UQ8oU1NgQ",
              "BQACAgIAAxkBAAIbt2ex9txtem5NhhS32_Gs9qKn6kxZAAJNWwAC7iAoSg2kOAm0G1WbNgQ",
              "BQACAgIAAxkBAAIbrWex9tyDdsjc4ta41MVyxDm_2BHzAAIzWgAC7iAoShaShW7Rhp1FNgQ",
              "BQACAgIAAxkBAAIbu2ex9twPGEVxFOjMuGbER3qen2FEAAKNWwAC7iAoSnOUiUU8gCFsNgQ",
              "BQACAgIAAxkBAAIbw2ex9twTTL2USXO8pe2wHiB8Z_QhAAL1VAACRDtRSpDsS98ynBbjNgQ",
              "BQACAgIAAxkBAAIbmmex9tx4m1go8gABUqmyCr87CjcaxwACelgAAu4gKEqpX0Lv3GjBBTYE",
              "BQACAgIAAxkBAAIbwWex9txf4WqZwgc0sXfZ37YmQo0OAAIwXAAC7iAoSvrJXrOWy038NgQ",
              "BQACAgIAAxkBAAIbuWex9twta1kAAYJ1Kn01TKRQ0OMbOAACi1sAAu4gKEqrZUXQuifJnDYE",
              "BQACAgIAAxkBAAIbxWex9tyvkQpwnaSLtl1eU33JqGg0AAL3ZwACrvPBSw9HOEpsURnINgQ",
              "BQACAgIAAxkBAAIbpGex9tzo-IqTzxtwSj2DftEazdh1AAJmWQAC7iAoSqw0bJNxtQ4fNgQ",
              "BQACAgIAAxkBAAIboGex9tzBmNj-XrWPnPyCvHsjIsVuAAKBWAAC7iAoSiNpjOBe93vxNgQ",
              "BQACAgIAAxkBAAIblmex9tzOsv1KmMvd4EsSzrmoDDDaAAKSVwAC7iAoSuWHZ4oOo3v7NgQ",
              "BQACAgIAAxkBAAIbqGex9twlqUERWNG6yPgpH8YzB90EAAIuWgAC7iAoSgXJ7qvMyWPANgQ",
              "BQACAgIAAxkBAAIbomex9tzwYrh2FShWHo6MWjPOW4TgAAIqWQAC7iAoSkxgms8d30laNgQ",
              "BQACAgIAAxkBAAIbv2ex9tzPK7Hd1wJRETotuzBpbhaOAALXWwAC7iAoSqPxrkGax0D6NgQ",
              "BQACAgIAAxkBAAIbnGex9twQqZ6_5Mi-9L4hD8WG9ZECAAJ8WAAC7iAoSi9TIwUf0LsaNgQ",
              "BQACAgIAAxkBAAIbpmex9twNlvpkzYrppMjbM-Cs8sxFAAIsWgAC7iAoSoFUPjMQSCemNgQ",
              "BQACAgIAAxkBAAIbqmex9tw3AAFZZXgJpF3csTjgU2NcMQACMFoAAu4gKEpMmkvmsWwX3jYE",
              "BQACAgIAAxkBAAIbtmex9txq-0EnlwaBQ4n132yD2FGlAAIqWwAC7iAoSirOBS4iWm-FNgQ",
              "BQACAgIAAxkBAAIblGex9txX-TyZ58cp-rOWK1fqel9cAAKQVwAC7iAoSuCiSjSpP-LnNgQ",
              "BQACAgIAAxkBAAIbrGex9tztcdC-Gy8q3rJPTbZB6AjHAAIyWgAC7iAoSvbfvAaSXzycNgQ",
              "BQACAgIAAxkBAAIbvmex9txI9mTg9uZiAkNpJ6wl51MyAALWWwAC7iAoSiTT9GwVOElBNgQ",
              "BQACAgIAAxkBAAIbsmex9tzefv3DDPlStaTnupZany7vAAIkWwAC7iAoSgFe3IcAAd0PsTYE",
              "BQACAgIAAxkBAAIbwGex9tyfTeL9vvEBT915kdxCKt_EAAILXAAC7iAoSh96q5gOxzAkNgQ",
              "BQACAgIAAxkBAAIbmGex9tw7FOi37YgjfTyk346QsJtvAAKUVwAC7iAoSiloPywxSV3mNgQ",
              "BQACAgIAAxkBAAIbvGex9twK3t1p7E4m3g04YXvUQlbkAAKOWwAC7iAoSk6HbKDeTCcaNgQ",
              "BQACAgIAAxkBAAIbkmex9tzTDh-5f-xMNuOeWK1XXvA7AAKOVwAC7iAoSgGZ6tgiHbjrNgQ",
              "BQACAgIAAxkBAAIbnmex9txjGCtNDmNP_37ddpBYqOguAAJ-WAAC7iAoSifUp4LIQbt2NgQ",
              "BQACAgIAAxkBAAIbumex9tzALRjF55MCMJJUs5Qh2jfZAAKMWwAC7iAoSiRDiezaAei0NgQ",
              "BQACAgIAAxkBAAIbuGex9tx8W59iBJqY0TV-0VmvIsk3AAKIWwAC7iAoSsmencH60G5lNgQ",
              "BQACAgIAAxkBAAIbwmex9txVcgomR50_y2sD2aML78hJAAIxXAAC7iAoSssGNjGmljA-NgQ",
              "BQACAgIAAxkBAAIbxGex9tx_6HlBe-0fSA59qzD7KbOGAAITUAAClMRgShgoIz9O9BvVNgQ",
              "BQACAgIAAxkBAAIbsGex9twHelkN_CkVew8B6OzcKw77AAI2WgAC7iAoSmDMuVHpuFkXNgQ",
              "BQACAgIAAxkBAAIbtGex9twwnvaM1OqDhOWtqN_7zWpZAAInWwAC7iAoSg2FG8_CZUM2NgQ",
              "BQACAgIAAxkBAAIbrmex9tzBUXxVo0_1Fja7KPHaZSWhAAI0WgAC7iAoSvOM9Ip1AUGSNgQ"
               ]

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