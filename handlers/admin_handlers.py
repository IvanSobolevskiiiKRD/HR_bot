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
from main import bot, main_admin, name_bot

router = Router()

class data_new_vakans(StatesGroup):
    job_type = State()
    name = State()
    descript = State()
    second_descript = State()
    photo = State()

class get_info_message(StatesGroup):
    message = State()
    id_candidat = State()

class find_user(StatesGroup):
    username = State()
    phone = State()

class Del_vakan(StatesGroup):
    url = State()

async def get_random_link():
    data_vakans = await rq.get_data_all_vacant()
    random_vakan_link = random.randint(1000, 10000)
    for vakan in data_vakans:
        if str(random_vakan_link) == vakan.link:
            await get_random_link()
    return random_vakan_link

async def generet_text_info_user(info_user):
    data_vakan = await rq.get_data_one_job(info_user["vakansion"])
    if data_vakan:
        data_vakan = data_vakan.__dict__
        vakan_name = data_vakan["name"]
    else:
        vakan_name = "Не выбрал"

    if info_user["name_surname"]:
        name_surname = info_user["name_surname"]
    else:
        name_surname = "Не указано"
    
    if info_user["number"]:
        number = info_user["number"]
    else:
        number = "Не указано"

    if info_user["city"]:
        city = info_user["city"]
    else:
        city = "Не указано"

    if info_user["citizenship"]:
        citizenship = info_user["citizenship"]
    else:
        citizenship = "Не указано"

    if info_user["birthday"]:
        birthday = info_user["birthday"]
    else:
        birthday = "Не указано"
    
    text_itog = text.format_info_abote_user.format(info_user["username"], name_surname, number, city,
                                                   citizenship, birthday, vakan_name)
    return text_itog


async def generete_history_message(data_user, new_message, status_Admin):
    data_now = datetime.now()
    time_text = data_now.strftime("%Y.%m.%d %H:%M")

    chat_history = data_user["chatHistory"]
    if chat_history == None:
        start_text = ""
        chat_history = ""
    else:
        start_text = "\n\n"
    
    if status_Admin:
        status_user = "Администратор"
    else:
        status_user = "Кандидат"

    form_itog = f"""{time_text} | {status_user}:
<blockquote>{new_message}</blockquote>
"""
    text_itog = chat_history + start_text + form_itog
    return text_itog


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

@router.callback_query(F.data == "find_user")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await callback.message.answer(text.find_user, reply_markup=admin_kb.find_user)

@router.callback_query(F.data.contains("find_user:username"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(find_user.username)
        await callback.message.answer(text.find_user_by_username, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data == "find_user:phone")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(find_user.phone)
        await callback.message.answer(text.find_user_by_number, reply_markup=admin_kb.back_admin)

@router.callback_query(F.data.contains("find_user_info:"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        _, user_id = callback.data.split(":")
        data_user = (await rq.get_data_one_user_by_id_user(user_id)).__dict__
        text_for_answer = await generet_text_info_user(data_user)
        await callback.message.answer(text=text_for_answer, reply_markup=await admin_kb.gen_info_kb(data_user["tg_id"]))

@router.callback_query(F.data.contains("history_with_user:"))
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        _, user_id = callback.data.split(":")
        data_user = (await rq.get_data_one_user(user_id)).__dict__
        await callback.message.answer(text.history_generate_text.format(data_user["chatHistory"]), reply_markup=await admin_kb.gen_history_kb(data_user["tg_id"]))

@router.callback_query(F.data == "skip_send_photo")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(photo = None)
        await callback.message.answer(text.answer_deskript_vakan, reply_markup=admin_kb.back_admin)
        await state.set_state(data_new_vakans.descript)

@router.callback_query(F.data == "list_vakan")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        data_all_vak = await rq.get_data_all_vacant()
        text_itog = ""
        for vak in data_all_vak:
            vak = vak.__dict__
            name = vak["name"]
            url = f"http://t.me/{name_bot}?start=vak_{vak["link"]}"
            text_itog = text_itog + f"{name} - {url}\n\n"
        await callback.message.answer(text = text.list_admin_vakan.format(text_itog), reply_markup= admin_kb.back_admin)

@router.callback_query(F.data == "del_vakan")
async def start(callback: CallbackQuery, state: FSMContext):
    user_data = await rq.get_data_one_user(callback.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.set_state(Del_vakan.url)
        await callback.message.answer(text.write_link_vakan, reply_markup = admin_kb.back_admin)

@router.message(Del_vakan.url)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        if "vak_" in message.text:
            url = (message.text.split("vak_"))[-1]
            try:
                data_job = (await rq.get_data_one_job_by_link(url)).__dict__
                await rq.delet_one_job(data_job["id"])
                await message.answer(text.success_delit_job.format(data_job["name"]))
                await state.clear()
            except:
                await message.answer(text.not_correct_write_link_job, reply_markup=admin_kb.back_admin)
        else:
            await message.answer(text.not_correct_write_link_job, reply_markup=admin_kb.back_admin)

@router.message(find_user.phone)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        try:
            number = int(message.text)
            if len(message.text) >= 4:
                all_users = await rq.get_all_finder_user(number)
                if all_users:
                    await message.answer(text.find_itog_phone.format(message.text), reply_markup=await admin_kb.gen_kb_find_users_by_number(all_users))
                    await state.clear()
                else:
                    await message.answer(text.not_find_user, reply_markup=admin_kb.back_admin)
        except:
            await message.answer(text.not_correct_write_phone, reply_markup=admin_kb.back_admin)

@router.message(find_user.username)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        all_users = await rq.get_all_finder_user_by_username(message.text)
        if all_users:
            await message.answer(text.find_itog_phone.format(message.text), reply_markup=await admin_kb.gen_kb_find_users_by_number(all_users))
            await state.clear()
        else:
            await message.answer(text.not_find_user_by_username, reply_markup=admin_kb.back_admin)

@router.message(get_info_message.message)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        data_states = await state.get_data()
        data_user = await rq.get_data_one_user(data_states["id_candidat"])
        data_user = data_user.__dict__
        if message.photo:
            text_admin = f"Администратор отправил фото и текст - {message.caption}"
        elif message.document:
            text_admin = f"Администратор отправил документ и текст - {message.caption}"
        elif message.video:
            text_admin = f"Администратор отправил видео и текст - {message.caption}"
        else:
            text_admin = message.html_text
        chat_history = await generete_history_message(data_user, text_admin, True)
        await rq.redact_data_user(data_user["tg_id"], "chatHistory", chat_history)
        await bot.copy_message(data_states["id_candidat"], message.chat.id, message.message_id)
        await message.answer(text.success_send_forvad_message)
        await state.clear()

@router.message(data_new_vakans.name)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(name = message.text)
        await message.answer(text.answer_photo_vakan, reply_markup=admin_kb.skip_send_photo)
        await state.set_state(data_new_vakans.photo)

@router.message(data_new_vakans.photo)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        if message.photo:
            await state.update_data(photo = message.photo[-1].file_id)
            await message.answer(text.answer_deskript_vakan, reply_markup=admin_kb.back_admin)
            await state.set_state(data_new_vakans.descript)
        else:
            await message.answer(text.not_correct_photo, reply_markup=admin_kb.back_admin)

@router.message(data_new_vakans.descript)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(descript = message.html_text)
        data_state = await state.get_data()
        if data_state["job_type"] == "3" or data_state["job_type"] == "2":
            await state.set_state(data_new_vakans.second_descript)
            await message.answer(text.write_second_descript, reply_markup=admin_kb.back_admin)
            return
        link_vakan = await get_random_link()
        await rq.set_job(name = data_state["name"], jobType = data_state["job_type"], description = data_state["descript"],
                         link = link_vakan, photo=data_state["photo"])
        await message.answer(text.new_vakan.format(f"http://t.me/{name_bot}?start=vak_{link_vakan}"))
        await state.clear()

@router.message(data_new_vakans.second_descript)
async def have_phNumb(message: Message, state: FSMContext):
    user_data = await rq.get_data_one_user(message.from_user.id)
    user_data = user_data.__dict__
    if user_data["isAdmin"]:
        await state.update_data(second_descript = message.html_text)
        data_state = await state.get_data()
        link_vakan = await get_random_link()
        await rq.set_job(name = data_state["name"], jobType = data_state["job_type"], description = data_state["descript"],
                         link = link_vakan, photo=data_state["photo"], second_descript= data_state["second_descript"])
        await message.answer(text.new_vakan.format(f"http://t.me/{name_bot}?start=vak_{link_vakan}"))
        await state.clear()