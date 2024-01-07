from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Импортируем настройки из config.py
from config import settings

# Создание асинхронного движка
engine = create_async_engine(settings.database_url, echo=True)  # Установи `echo=False` в продакшене

# Создание фабрики асинхронных сессий
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

# Функция для создания асинхронной сессии
async def get_async_session():
    async with async_session() as session:
        yield session