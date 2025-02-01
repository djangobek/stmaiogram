from aiogram.filters.state import State,StatesGroup
class ReklamaState(StatesGroup):
    add = State()
    check = State()
class TextState(StatesGroup):
    text = State()
    url = State()
    check = State()
class ImageState(StatesGroup):
    image = State()
    url = State()
    check = State()
class VideoState(StatesGroup):
    video = State()
    url = State()
    check = State()
class AddChannelState(StatesGroup):
    id = State()
    check = State()


class Namesurname(StatesGroup):
    full_name = State()

class Oddiy_testState(StatesGroup):
    answers = State()

class check_oddiy_testState(StatesGroup):
    code  = State()
    answers = State()


class FanliTestState(StatesGroup):
    name = State()
    answers = State()