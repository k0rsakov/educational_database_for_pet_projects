import logging

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def generate_db_uri(
        host: str = "localhost",
        port: int=5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres", # noqa: S107
) -> str:
    """
    Создание строки подключения к БД PostgreSQL.

    :param host: Хост; default: `localhost`
    :param port: Порт; default: `5432`
    :param database: Название базы данных; default: `postgres`
    :param user: Пользователь; default: `postgres`
    :param password: Пароль; default: `postgres`
    :return:
    """

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def pg_connect_uri(
        host: str = "localhost",
        port: int=5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres", # noqa: S107
) -> Engine:
    """
    Создание подключения к БД PostgreSQL.

    :param host: Хост; default: `localhost`.
    :param port: Порт; default: `5432`.
    :param database: Название базы данных; default: `postgres`.
    :param user: Пользователь; default: `postgres`.
    :param password: Пароль; default: `postgres`.
    :return:
    """
    db_uri = generate_db_uri(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )

    return create_engine(db_uri)

def run_query(
        engine: Engine = None,
        sql: str | None = None,
) -> None:
    """
    Выполняет SQL-код.

    :param engine: Движок БД; default: `None`.
    :param sql: SQL-код; default: `None`.
    :return:
    """

    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()
