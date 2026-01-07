from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq
import math

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить пробный урок 🆓', callback_data="sign_up_for_trial_lesson")],
    [InlineKeyboardButton(text='Мои ученики 👩🏻‍🎓', callback_data="Students"),
    InlineKeyboardButton(text='Мои достижения 🏆', callback_data="achievements")],
    [InlineKeyboardButton(text='Я в сети 🌐', callback_data="i_online"),
    InlineKeyboardButton(text='Что тебя ждёт ✨', callback_data="individual_plan")],
    [InlineKeyboardButton(text='Мой подход 🗂', callback_data="my_approach")]
])

start_kb_after_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Задать вопрос ✒️', url="https://t.me/SobolevskiiiI")],
    [InlineKeyboardButton(text='Мои ученики 👩🏻‍🎓', callback_data="Students"),
    InlineKeyboardButton(text='Мои достижения 🏆', callback_data="achievements")],
    [InlineKeyboardButton(text='Я в сети 🌐', callback_data="i_online"),
    InlineKeyboardButton(text='Что тебя ждёт ✨', callback_data="individual_plan")],
    [InlineKeyboardButton(text='Мой подход 🗂', callback_data="my_approach")]
])

back_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад ⬅️', callback_data="main")]
])