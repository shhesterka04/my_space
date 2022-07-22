import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

user_data = {'name': "0", 'gener': '1', 'weight': '2',
             'growth': '3', 'age': '4', 'lifestyle': '5',
             'frequency': '6', 'water': '7', 'semifinished ': '8',
             'gadget': '9', 'gender': '10', 'special': '11'}

gender_var = []
lifestyle = []
frequency = []
semifinished = []

BOT_TOKEN = "5545559941:AAEQIdFRC8U-X5Rk2H8MKb9uJnkIXQIK7uI"
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


class UserState(StatesGroup):
    # name = State()
    # goal = State()
    # gender = State()
    # weight = State()
    # growth = State()
    # age = State()
    # lifestyle = State()
    # frequency = State()
    # gadget = State()
    # special = State()

    name = State()
    address = State()


@dp.message_handler(commands="quiz")
async def quiz(message: types.Message):
    await message.answer("(1/10) Как к вам обращаться?")
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично! Теперь введите ваш адрес.")
    await UserState.next()  # либо же UserState.adress.set()


@dp.message_handler(state=UserState.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data['username']}\n"
                         f"Адрес: {data['address']}")

    await state.finish()

    await state.update_data(username=message.text)
    # await message.answer("(2/10) Какая у вас цель по питанию?")
    # await message.answer("(3/10) Какой у вас пол?")
    # await message.answer("(4/10) Сколько вы весите")
    # await message.answer("(5/10) Какой у вас рост в сантиметрах?")
    # await message.answer("(6/10) Сколько вам лет?")
    # await message.answer("(7/10) Какой у вас образ жизни?")
    # await message.answer("(8/10) Ко скольким приемам пищи вы приквыкли?")
    # await message.answer("(9/10) Какие инструменты у вас есть?")
    # await message.answer("(10/10) У вас есть какие-то противопоказния и пожелания?")


dp.register_message_handler(quiz, commands="quiz")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.answer("Привет!\nНадоело думать о том, что бы такого приготовить?\n " +
                         "Я тебе помогу! Я знаю кучу рецептов на любой вкус, умею составлять индидуальные" +
                         "рационы на неделю и не только!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_1 = types.KeyboardButton(text="Конечно!")
    keyboard.add(button_1)
    await message.answer("Перед тем как начать работу, можно я задам тебе несколько" +
                         "вопросов для составления идеального рациона питания для тебя?", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Конечно!"))
    async def with_puree(message: types.Message):
        await message.reply("Супер!")
        await quiz(message)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
