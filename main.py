import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from api.APIService import APIService
from localization_service.LocalesManager import LanguageManager
from localization_service.i18n import i18n
from search_nft_service.SearchStateManager import SearchStateManager

load_dotenv()


bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()

# Инициализация синглтонов
api_service = APIService()

SearchStateManager()

i18n()
LanguageManager()



async def main():
    # entrypoint
    await dp.start_polling(bot)
    await api_service.close_session()



if __name__ == "__main__":
    asyncio.run(main())
