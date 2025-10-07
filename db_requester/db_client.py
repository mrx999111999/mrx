from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DataBaseCreds
from sqlalchemy.orm import Session as SASession

DB_USER = DataBaseCreds.DB_USER
DB_PASSWORD = DataBaseCreds.DB_PASSWORD
DB_HOST = DataBaseCreds.DB_HOST
DB_PORT = DataBaseCreds.DB_PORT
DB_NAME = DataBaseCreds.DB_NAME

#  Движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

#  Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> SASession:
    """Создает новую сессию БД"""
    return SessionLocal()
