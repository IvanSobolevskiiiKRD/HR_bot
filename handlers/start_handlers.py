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
from main import bot, main_admin

router = Router()



class Forms_for_jobType1(StatesGroup):
    number = State()
    name_surname = State()
    city = State()
    citizenship = State()
    birthday = State()

class Forms_for_jobType2(StatesGroup):
    number = State()

class Write_admin(StatesGroup):
    message = State()

async def generete_history_message(data_user, new_message):
    data_now = datetime.now()
    time_text = data_now.strftime("%Y.%m.%d %H:%M")

    chat_history = data_user["chatHistory"]
    if chat_history == None:
        start_text = ""
        chat_history = ""
    else:
        start_text = "\n\n"
    
    if data_user["isAdmin"]:
        status_user = "Администратор"
    else:
        status_user = "Кандидат"

    form_itog = f"""{time_text} | {status_user}:
<blockquote>{new_message}</blockquote>
"""
    text_itog = chat_history + start_text + form_itog
    return text_itog


#ГЛАВНОЕ МЕНЮ НАЧАЛО
@router.message(CommandStart())
async def start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    await rq.set_user(message.from_user.id, message.from_user.username)
    data_user = await rq.get_data_one_user(message.from_user.id)
    data_user = data_user.__dict__

    #if data_user["vakansion"]:
    #    pass
    #else:
    #    return
    
    if command.args:
        option, value = command.args.split("_")
        data_vakan = await rq.get_data_one_job_by_link(value)
        if data_vakan == None:
            jobs_list = await rq.get_data_all_vacant()
            await message.answer(text=text.start_message, reply_markup=await start_kb.gen_kb_start(jobs_list))
            return

        data_vakan = data_vakan.__dict__
        await rq.redact_data_user(message.from_user.id, "vakansion", data_vakan["id"])
        if data_vakan["jobType"] == 3:
            await message.answer(text=data_vakan["description"], reply_markup=start_kb.apply_form_for_jB3)
        if data_vakan["jobType"] == 2:
            await message.answer(text=data_vakan["description"], reply_markup=start_kb.apply_form_for_jB2)
        if data_vakan["jobType"] == 1:
            await message.answer(text=data_vakan["description"], reply_markup=start_kb.apply_form_for_jB1)
        return
    
    jobs_list = await rq.get_data_all_vacant()
    await message.answer(text=text.start_message, reply_markup=await start_kb.gen_kb_start(jobs_list))

@router.callback_query(F.data.contains("vakansion_"))
async def vakan(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data
    _,vakan_id = callback_data.split("_")
    await rq.redact_data_user(callback.from_user.id, "vakansion", vakan_id)
    data_vakan = await rq.get_data_one_job(int(vakan_id))
    data_vakan = data_vakan.__dict__
    if data_vakan["jobType"] == 3:
        await callback.message.answer(text=data_vakan["description"], reply_markup=start_kb.apply_form_for_jB3)
    if data_vakan["jobType"] == 2:
        await callback.message.answer(text=data_vakan["description"], reply_markup=start_kb.apply_form_for_jB2)
    if data_vakan["jobType"] == 1:
        await callback.message.answer(text=data_vakan["description"], reply_markup=start_kb.apply_form_for_jB1)
        

@router.callback_query(F.data == "write_administrator")
async def vakan(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Write_admin.message)
    await callback.message.answer(text.write_admin_text)

@router.callback_query(F.data == "jobType1")
async def vakan(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Forms_for_jobType1.number)
    await callback.message.answer(text=text.ask_phone_number)

@router.callback_query(F.data == "jobType2")
async def vakan(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Forms_for_jobType2.number)
    await callback.message.answer(text=text.ask_phone_number)

@router.callback_query(F.data == "jobType3")
async def vakan(callback: CallbackQuery, state: FSMContext):
    data_user = await rq.get_data_one_user(callback.from_user.id)
    data_user = data_user.__dict__
    data_vakan = await rq.get_data_one_job(data_user["vakansion"])
    data_vakan = data_vakan.__dict__
    await callback.message.answer(text=data_vakan["secondDescription"], reply_markup=start_kb.write_administrator)


@router.message(Write_admin.message)
async def have_phNumb(message: Message, state: FSMContext):
    data_all_user = await rq.get_data_all_user()
    data_user = await rq.get_data_one_user(message.from_user.id)
    data_user = data_user.__dict__
    chat_history = await generete_history_message(data_user, message.text)
    await rq.redact_data_user(message.from_user.id, "chatHistory", chat_history)

    for user in data_all_user:
        if user.isAdmin:
            if user.name_surname:
                name = user.name_surname
            else:
                name = "Не указано"
            if user.number:
                number = user.number
            else:
                number = "Не указано"
            await bot.send_message(user.tg_id, text=text.form_answer_to_admin.format(
                name, number, message.from_user.username, message.html_text
            ), reply_markup=await start_kb.gen_admin_answer_kb(message.from_user.id))
            
    await message.answer(text.success_send_to_admin)
    await state.clear()

@router.message(Forms_for_jobType1.number)
async def have_phNumb(message: Message, state: FSMContext):
    await state.update_data(number = message.text)
    await state.set_state(Forms_for_jobType1.name_surname)
    await message.answer(text=text.ask_name_surname)

@router.message(Forms_for_jobType1.name_surname)
async def have_phNumb(message: Message, state: FSMContext):
    await state.update_data(name_surname = message.text)
    await state.set_state(Forms_for_jobType1.city)
    await message.answer(text=text.ask_city)

@router.message(Forms_for_jobType1.city)
async def have_phNumb(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    await state.set_state(Forms_for_jobType1.citizenship)
    await message.answer(text=text.ask_citizenship)

@router.message(Forms_for_jobType1.citizenship)
async def have_phNumb(message: Message, state: FSMContext):
    await state.update_data(citizenship = message.text)
    await state.set_state(Forms_for_jobType1.birthday)
    await message.answer(text=text.ask_birthday)

@router.message(Forms_for_jobType1.birthday)
async def have_phNumb(message: Message, state: FSMContext):
    await state.update_data(birthday = message.text)
    old_data_states = await state.get_data()
    await rq.redact_data_user(message.from_user.id, "number", old_data_states["number"])
    await rq.redact_data_user(message.from_user.id, "name_surname", old_data_states["name_surname"])
    await rq.redact_data_user(message.from_user.id, "city", old_data_states["city"])
    await rq.redact_data_user(message.from_user.id, "citizenship", old_data_states["citizenship"])
    await rq.redact_data_user(message.from_user.id, "birthday", old_data_states["birthday"])
    await message.answer(text=text.end_text, reply_markup=start_kb.write_administrator)
    await state.clear()

@router.message(F.text)
async def have_phNumb(message: Message):
    data_all_user = await rq.get_data_all_user()
    data_user = await rq.get_data_one_user(message.from_user.id)
    data_user = data_user.__dict__
    chat_history = await generete_history_message(data_user, message.text)
    await rq.redact_data_user(message.from_user.id, "chatHistory", chat_history)

    for user in data_all_user:
        if user.isAdmin:
            if user.name_surname:
                name = user.name_surname
            else:
                name = "Не указано"
            if user.number:
                number = user.number
            else:
                number = "Не указано"
            await bot.send_message(user.tg_id, text=text.form_answer_to_admin.format(
                name, number, message.from_user.username, message.html_text
            ), reply_markup=await start_kb.gen_admin_answer_kb(message.from_user.id))