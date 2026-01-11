from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import math
import random

from keybords import admin_kb
import text
import database.requests as rq
from main import bot, main_admin

router = Router()

class data_new_vakans(StatesGroup):
    job_type = State()
    name = State()
    descript = State()
    second_descript = State()

class get_info_message(StatesGroup):
    message = State()
    id_candidat = State()

class find_user(StatesGroup):
    username = State()
    phone = State()

async def get_random_link():
    data_vakans = await rq.get_data_all_vacant()
    random_vakan_link = random.randint(1000, 10000)
    for vakan in data_vakans:
        if str(random_vakan_link) == vakan.link:
            await get_random_link()
    return random_vakan_link


@router.message(Command("admin"))
async def start(message: Message, command: CommandObject, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.clear()
        await message.answer(text= text.admin_welcome, reply_markup=admin_kb.main_kb)

@router.callback_query(F.data == "back_admin")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.clear()
        await callback.message.answer(text= text.admin_welcome, reply_markup=admin_kb.main_kb)

@router.callback_query(F.data == "create_vakan")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await callback.message.answer(text.create_new_vakan, reply_markup=admin_kb.vakans_tips)

@router.callback_query(F.data == "create_vakat_tips_1")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(data_new_vakans.job_type)
        await state.update_data(job_type="1")
        await state.set_state(data_new_vakans.name)
        await callback.message.answer(text.answer_name_vakan, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data == "create_vakat_tips_2")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(data_new_vakans.job_type)
        await state.update_data(job_type="2")
        await state.set_state(data_new_vakans.name)
        await callback.message.answer(text.answer_name_vakan, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data == "create_vakat_tips_3")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(data_new_vakans.job_type)
        await state.update_data(job_type="3")
        await state.set_state(data_new_vakans.name)
        await callback.message.answer(text.answer_name_vakan, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data.contains("answer_kandidat_"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        _, _, telegram_id = callback.data.split("_")
        await state.set_state(get_info_message.id_candidat)
        await state.update_data(id_candidat = telegram_id)
        await state.set_state(get_info_message.message)
        await callback.message.answer(text.write_you_answer_admin)

@router.callback_query(F.data.contains("find_user"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await callback.message.answer(text.find_user, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data.contains("find_user:username"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(find_user.username)
        await callback.message.answer(text.find_user_by_username, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data.contains("find_user:phone"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(find_user.phone)
        await callback.message.answer(text.find_user_by_number, reply_markup=admin_kb.back_admin)

@router.message(find_user.phone)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        try:
            number = int(message.text)
            if len(number) >= 4:
                pass
        except:
            await message.answer(text.not_correct_write_phone)

@router.message(get_info_message.message)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        data_states = await state.get_data()
        await bot.forward_message(data_states["id_candidat"], message.chat.id, message.message_id)
        await message.answer(text.success_send_forvad_message)
        await state.clear()

@router.message(data_new_vakans.name)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(name = message.text)
        await message.answer(text.answer_deskript_vakan, reply_markup=admin_kb.back_admin)
        await state.set_state(data_new_vakans.descript)

@router.message(data_new_vakans.descript)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(descript = message.text)
        data_state = await state.get_data()
        if data_state["job_type"] == "3":
            await state.set_state(data_new_vakans.second_descript)
            await message.answer(text.write_second_descript, reply_markup=admin_kb.back_admin)
            return
        link_vakan = await get_random_link()
        await rq.set_job(name = data_state["name"], jobType = data_state["job_type"], description = data_state["descript"],
                         link = link_vakan)
        await message.answer(text.new_vakan)
        await state.clear()

@router.message(data_new_vakans.second_descript)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(second_descript = message.text)
        data_state = await state.get_data()
        link_vakan = await get_random_link()
        await rq.set_job(name = data_state["name"], jobType = data_state["job_type"], description = data_state["descript"],
                         link = link_vakan, second_descript= data_state["second_descript"])
        await message.answer(text.new_vakan.format(f"http://t.me/Test_Moroz12333_bot?start=vak_{link_vakan}"))
        await state.clear()