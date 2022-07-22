import logging
import json
from os import getenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

class UserState(StatesGroup):
    name = State()
    goal = State()
    gender = State()
    weight = State()
    growth = State()
    age = State()
    lifestyle = State()
    frequency = State()
    gadgets = State()
    special = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.answer("Привет!\nНадоело думать о том, что бы такого приготовить?\n " +
                         "Я тебе помогу! Я знаю кучу рецептов на любой вкус, умею составлять индидуальные" +
                         "рационы на неделю и не только!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Конечно!")
    await message.answer("Перед тем как начать работу, можно я задам тебе несколько" +
                         "вопросов для составления идеального рациона питания для тебя?", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Конечно!"))
    async def with_puree(message: types.Message):
        await message.reply("Супер!")
        await new_user(message)


@dp.message_handler(commands="reg")
async def new_user(message: types.Message):
    await message.answer("(1/10) Как к вам обращаться?")
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    var = ['Похудеть', "Набрать массу", "Сохранить"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for temp in var:
        keyboard.add(temp)
    await message.answer("(2/10) Какая у вас цель по питанию?", reply_markup=keyboard)
    await UserState.next()



@dp.message_handler(state=UserState.goal)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    var = ['М', "Ж"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for temp in var:
        keyboard.add(temp)
    await message.answer("(3/10) Какой у вас пол?", reply_markup=keyboard)
    await UserState.next()


@dp.message_handler(state=UserState.gender)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("(4/10) Сколько вы весите?")
    await UserState.next()


@dp.message_handler(state=UserState.weight)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer("(5/10) Какой у вас рост в сантиметрах?")
    await UserState.next()


@dp.message_handler(state=UserState.growth)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("(6/10) Сколько вам лет?")
    await UserState.next()


@dp.message_handler(state=UserState.age)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    var = [
        'Часто не прохожу и 7 000 шагов за день',
        'Работаю сидя, стабильно прохожу 10 000 шагов',
        'Занимаюсь физ. нагрузкой 1-2 часа в неделю',
        'Занимаюсь физ.нагрузкой 3-5 часов в неделю',
        'Занимаюсь спортом больше 5 часов в неделю]'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for temp in var:
        keyboard.add(temp)
    await message.answer("(7/10) Какой у вас образ жизни?", reply_markup=keyboard)

    await UserState.next()


@dp.message_handler(state=UserState.lifestyle)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(lifestyle=message.text)
    var = ['2', '3', '4', '5', '6']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for temp in var:
        keyboard.add(temp)
    await message.answer("(8/10) Ко скольким приемам пищи вы привыкли?", reply_markup=keyboard)

    await UserState.next()


@dp.message_handler(state=UserState.frequency)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(frequency=message.text)
    var = ['СВЧ печь', 'блендер', 'духовка', 'плита', 'мультиварка']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for temp in var:
        keyboard.add(temp)
    await message.answer("(9/10) Какие инструменты у вас есть?", reply_markup=keyboard)

    await UserState.next()


@dp.message_handler(state=UserState.gadgets)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(gadgets=message.text)
    var = ["Не ем глютен", "Я веган", "Я вегетарианец", "Не ем глюкозу"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for temp in var:
        keyboard.add(temp)
    await message.answer("(10/10) У вас есть какие-то противопоказния и пожелания?", reply_markup=keyboard)

    await UserState.next()

@dp.message_handler(state=UserState.special)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(special=message.text)
    data = await state.get_data()
    data = json.dumps(data)
    await message.answer(data)

    await state.finish()

dp.register_message_handler(new_user, commands="reg")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

