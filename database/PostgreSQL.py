import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def pg_connect_uri(
        host: str = "localhost",
        port: int=5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres", # noqa: S107
) -> Engine:
    """
    Создание подключения к БД PostgreSQL.

    :param host: Хост; default: `localhost`
    :param port: Порт; default: `5432`
    :param database: Название базы данных; default: `postgres`
    :param user: Пользователь; default: `postgres`
    :param password: Пароль; default: `postgres`
    :return:
    """
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    return create_engine(db_url)
