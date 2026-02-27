import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Подключаемся к БД
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:secretpassword@db:5432/todolist"
)

# Создаем "движок" SQLAlchemy — это главная точка входа для работы с БД
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем фабрику сессий. Сессия — это транзакция, через которую мы будем делать запросы (CRUD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс, от которого будут наследоваться все наши таблицы (модели)
Base = declarative_base()

# Эта функция будет создавать новую сессию БД для каждого запроса к нашему API
# и автоматически закрывать её после того, как запрос отработает.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()