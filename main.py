import asyncio
from Token import TOKEN
from aiogram import Bot, Dispatcher
from database.models import async_main
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

from handlers import start_handlers


async def main():
    await async_main()
    dp = Dispatcher()
    dp.include_router(start_handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())