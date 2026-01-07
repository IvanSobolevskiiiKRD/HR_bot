from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import math

from keybords import start_kb
import text
import database.requests as rq

router = Router()

class Demo_Day(StatesGroup):
    name = State()
    phone = State()

#ГЛАВНОЕ МЕНЮ НАЧАЛО
@router.message(CommandStart())
async def start(message: Message, command: CommandObject, state: FSMContext):
    await message.answer(text="Добро пожаловать")