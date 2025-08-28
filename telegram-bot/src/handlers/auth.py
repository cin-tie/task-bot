from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.auth_service import AuthService

router = Router()

class RegistrationStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_email = State()

@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    auth_service = AuthService()
    
    # Проверяем, не зарегистрирован ли пользователь
    telegram_id = str(message.from_user.id)
    user_exists = await auth_service.check_user_exists(telegram_id)
    
    if user_exists:
        await message.answer("✅ Вы уже зарегистрированы!")
        return
    
    # Начинаем процесс регистрации
    await state.set_state(RegistrationStates.waiting_for_password)
    await message.answer(
        "🔐 Придумайте пароль для вашего аккаунта:\n\n"
        "• Минимум 8 символов\n"
        "• Должен содержать буквы в верхнем и нижнем регистре\n"
        "• Должен содержать цифры\n"
        "• Должен содержать специальные символы"
    )

@router.message(RegistrationStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()
    
    # Простая валидация пароля
    if len(password) < 8:
        await message.answer("❌ Пароль слишком короткий. Минимум 8 символов.")
        return
    
    await state.update_data(password=password)
    await state.set_state(RegistrationStates.waiting_for_email)
    await message.answer(
        "📧 Укажите ваш email (необязательно):\n\n"
        "Или отправьте /skip чтобы пропустить"
    )

@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip() if message.text != "/skip" else None
    
    data = await state.get_data()
    password = data.get('password')
    
    auth_service = AuthService()
    telegram_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    
    try:
        result = await auth_service.register_user(
            telegram_id=telegram_id,
            username=username,
            password=password,
            email=email
        )
        
        if result.get('access_token'):
            await message.answer(
                "🎉 Регистрация успешна!\n\n"
                "Теперь вы можете получать ежедневные задания.\n"
                "Первое задание придет завтра в 12:00 ⏰"
            )
        else:
            await message.answer("❌ Ошибка регистрации. Попробуйте позже.")
            
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
    
    await state.clear()

@router.message(Command("login"))
async def cmd_login(message: Message, state: FSMContext):
    await message.answer(
        "🔐 Для входа укажите ваш пароль:"
    )
    # Здесь можно добавить логику входа