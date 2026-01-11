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


async def gen_kb_start(vak_list):
    key_board = InlineKeyboardBuilder()
    for vak in vak_list:
        
        vak = vak.__dict__
        name = str(vak["name"])
        callback = f"vakansion_{vak['id']}"
        key_board.row(InlineKeyboardButton(text=name, callback_data=callback))

    return key_board.as_markup()

async def gen_admin_answer_kb(tg_id):
    key_board = InlineKeyboardBuilder()
    key_board.row(InlineKeyboardButton(text="Ответить кандидату", callback_data=f"answer_kandidat_{tg_id}"))
    return key_board.as_markup()

apply_form_for_jB1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Заполнить форму', callback_data="jobType1")]
])

apply_form_for_jB2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Заполнить форму', callback_data="jobType2")]
])

apply_form_for_jB3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить ссылку для заполнения', callback_data="jobType3")]
])

write_administrator = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Написать администратору', callback_data="write_administrator")]
])