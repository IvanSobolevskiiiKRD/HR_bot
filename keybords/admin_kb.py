from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq
import math

main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать вакансию', callback_data="create_vakan")],
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

skip_send_photo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data="skip_send_photo")],
    [InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin")]
])

find_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти по username', callback_data="find_user:username")],
    [InlineKeyboardButton(text='Найти по номеру', callback_data="find_user:phone")],
    [InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin")]
])

async def gen_kb_find_users_by_number(users_list):
    key_board = InlineKeyboardBuilder()
    if len(users_list) >9:
        users_list = users_list[0:8]
    for user in users_list:
        user = user.__dict__
        name = f"{user["username"]} - {user["number"]} - {user["name_surname"]}"
        callback_data = f"find_user_info:{user["id"]}"
        key_board.row(InlineKeyboardButton(text=name, callback_data=callback_data))
    key_board.row(InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin"))
    return key_board.as_markup()

async def gen_info_kb(id_user):
    key_board = InlineKeyboardBuilder()
    key_board.row(InlineKeyboardButton(text='Написать пользователю', callback_data=f"answer_kandidat_{id_user}"))
    key_board.row(InlineKeyboardButton(text='Посмотреть историю чата', callback_data=f"history_with_user:{id_user}"))
    key_board.row(InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin"))
    return key_board.as_markup()

async def gen_history_kb(id_user):
    key_board = InlineKeyboardBuilder()
    key_board.row(InlineKeyboardButton(text='Написать пользователю', callback_data=f"answer_kandidat_{id_user}"))
    key_board.row(InlineKeyboardButton(text='🔙 Вернуться 🔙', callback_data="back_admin"))
    return key_board.as_markup()