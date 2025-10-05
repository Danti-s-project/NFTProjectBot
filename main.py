import asyncio


from api.APIService import APIService
from localization_service import i18n, LocalesManager
from search_nft_service.SearchStateManager import SearchStateManager
from utils.logging_setup import setup_logger
from courses_service.CoursesManager import CoursesManager
from dispatcher import dp, bot




# Настройка логирования
logger = setup_logger()


async def main():
    # Инициализация синглтонов
    api_service = APIService()

    SearchStateManager()

    i18n()
    LocalesManager()

    CoursesManager()

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
