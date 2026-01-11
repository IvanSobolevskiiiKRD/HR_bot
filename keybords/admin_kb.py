from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq
import math

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поздать вакансию', callback_data="create_vakan")],
    [InlineKeyboardButton(text='Найти пользователя', callback_data="find_user")]
])

vakans_tips = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вакансия с формой', callback_data="create_vakat_tips_1")],
    [InlineKeyboardButton(text='Вакансия только с номером', callback_data="create_vakat_tips_2")],
    [InlineKeyboardButton(text='Вакансия без данных', callback_data="create_vakat_tips_3")]
])

back_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin")]
])

find_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти по username', callback_data="find_user:username")],
    [InlineKeyboardButton(text='Найти по номеру', callback_data="find_user:phone")],
    [InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin")]
])