from database.models import async_session
from database.models import User, Jobs
from sqlalchemy import select, update, delete
from datetime import datetime

async def set_user(telegram_id, username):
    async with async_session() as session:
        start_data = datetime.now()
        user = await session.scalar(select(User).where(User.tg_id == telegram_id))

        if not user:
            session.add(User(tg_id=telegram_id, username=username, isAdmin=False,
                            vakansion=None, name_surname=None,
                            number=None, city=None, citizenship=None, 
                            birthday=None, chatHistory=None))
            await session.commit()
        
async def set_prob_zanatia(telegram_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"prob_zanatia": True}))
        await session.commit()

async def admin_cheak(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User.admin).where(User.tg_id == telegram_id))
    
async def set_admin(telegram_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"admin": True}))
        await session.commit()

async def get_data_all_user():
    async with async_session() as session:
        res =  await session.execute(select(User))
        return res.scalars().all()
    
async def get_data_one_user(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == telegram_id))
    
async def get_data_one_user_by_crm(crm_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.reg_user_lk_id_crm == crm_id))
    
async def get_data_one_user_by_id_user(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == user_id))
    
async def redact_data_user(tg_id, col, new_data):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(**{col: new_data}))
        await session.commit()


async def get_all_finder_user(phone): # Функция которая возвращает объекты из БД в которой нашелся соответсвующий номер телефона
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.number.contains(phone)))
        return result.all()

async def get_all_finder_user_by_username(username): # Функция которая возвращает объекты из БД в которой нашелся соответсвующий номер телефона
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.username.contains(username)))
        return result.all()


async def get_data_all_vacant():
    async with async_session() as session:
        res =  await session.execute(select(Jobs))
        return res.scalars().all()

async def get_data_one_job(id):
    async with async_session() as session:
        return await session.scalar(select(Jobs).where(Jobs.id == id))

async def get_data_one_job_by_link(link):
    async with async_session() as session:
        return await session.scalar(select(Jobs).where(Jobs.link == link))
    
async def set_job(name, description, link, jobType, photo, second_descript = False):
    async with async_session() as session:
        if jobType == "3":
            session.add(Jobs(name = name, jobType = jobType, description = description,
                             secondDescription = second_descript, link = link))
        if jobType == "2" or jobType == "1":
            session.add(Jobs(name = name, jobType = jobType, description = description,
                             link = link, photo = photo))
        await session.commit()