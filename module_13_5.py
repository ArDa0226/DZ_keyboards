from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age: int = State()
    growth: int = State()
    weight: int = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
information = KeyboardButton(text='Информация')
calories = KeyboardButton(text='Рассчитать')
kb.add(information)
kb.add(calories)
@dp.message_handler(text='Привет')
async def hello_message(message):
    await message.answer('Введите команду /start, чтобы начать диалог')

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я Бот, помогающий твоему здоровью. '
                         'Введите слово Calories.',
                         reply_markup= kb)
@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст.')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    calc_calories = (10 * int(data['third'])) + (6.25 * int(data['second'])) - (5 * int(data['first'])) + 5
    await message.answer(f'Ваша суточная норма каллорий составляет: {calc_calories} Ккал.')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)