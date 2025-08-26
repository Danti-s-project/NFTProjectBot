"""
Здесь все хендлеры команд бота
"""

from aiogram.filters.command import CommandStart
from aiogram.types import Message

from routers.start_router import StartRouter
from main import dp


@dp.message(CommandStart(deep_link=True))
async def start_command_handler(message: Message, command: CommandStart) -> None:
    """
    Хендлер для команды /start

    :param message: aiogram Message
    :return: None
    """
    router = StartRouter(message, command.args)
    await router.route()
