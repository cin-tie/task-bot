from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    await message.answer(
        "📋 Ваши задания:\n\n"
        "Здесь будет список ваших заданий...\n\n"
        "Ежедневные задания приходят в 12:00 ⏰"
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    await message.answer(
        "📊 Ваша статистика:\n\n"
        "• Выполнено заданий: 0\n"
        "• Текущая серия: 0 дней\n"
        "• Всего дней: 0\n\n"
        "Начните выполнять задания чтобы увидеть прогресс!"
    )