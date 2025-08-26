import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()


bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()

async def main():
    # entrypoint
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
