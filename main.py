import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from api.APIService import APIService

load_dotenv()


bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()
api_service = APIService()


async def main():
    # entrypoint
    await dp.start_polling(bot)
    await api_service.close_session()


if __name__ == "__main__":
    asyncio.run(main())
