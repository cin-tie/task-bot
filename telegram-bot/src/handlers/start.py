from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    welcome_text = (
        f"👋 Привет, {user.first_name}!\n\n"
        "Я бот для ежедневных заданий!\n\n"
        "📝 Каждый день в 12:00 я буду присылать тебе новое задание\n"
        "✅ Отмечай выполненные задания\n"
        "📊 Следи за своей статистикой\n\n"
        "Для начала работы зарегистрируйся командой /register"
    )
    await message.answer(welcome_text)