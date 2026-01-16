from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq
import math


back_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ В главное меню', callback_data="main")]
])


async def gen_kb_start(vak_list):
    key_board = InlineKeyboardBuilder()
    for vak in vak_list:
        vak = vak.__dict__
        name = str(vak["name"])
        callback = f"vakansion_{vak['id']}"
        key_board.row(
            InlineKeyboardButton(text=f"📌 {name}", callback_data=callback)
        )

    return key_board.as_markup()


async def gen_admin_answer_kb(tg_id):
    key_board = InlineKeyboardBuilder()
    key_board.row(
        InlineKeyboardButton(
            text="✍️ Ответить кандидату",
            callback_data=f"answer_kandidat_{tg_id}"
        )
    )
    return key_board.as_markup()


apply_form_for_jB1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝 Заполнить анкету', callback_data="jobType1")]
])

apply_form_for_jB2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝 Заполнить анкету', callback_data="jobType2")]
])

apply_form_for_jB3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔗 Получить ссылку для отклика', callback_data="jobType3")]
])

write_administrator = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📩 Написать администратору', callback_data="write_administrator")]
])

async def gen_kb_type_3(url):
    key_board = InlineKeyboardBuilder()
    key_board.row(InlineKeyboardButton(text="✍️ ЗАПОЛНИТЬ АНКЕТУ", url=url))
    return key_board.as_markup()