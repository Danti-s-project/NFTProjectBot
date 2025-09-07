import asyncio


from api.APIService import APIService
from localization_service.LocalesManager import LanguageManager
from localization_service.i18n import i18n
from search_nft_service.SearchStateManager import SearchStateManager
from utils.logging_setup import setup_logger
from dispatcher import dp, bot


# Настройка логирования
logger = setup_logger()


async def main():
    # Инициализация синглтонов
    api_service = APIService()

    SearchStateManager()

    i18n()
    LanguageManager()

    logger.info("Все сервисы инициализированы")

    # Прогружаем хендлеры
    import handler

    logger.info("Handlers was loaded.")

    # entrypoint
    logger.info("Запуск бота...")
    await dp.start_polling(bot)
    logger.info("Бот остановлен")
    await api_service.close_session()



if __name__ == "__main__":
    asyncio.run(main())
