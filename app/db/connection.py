
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.config import settings
from app.utils import db_logger
from contextlib import contextmanager


engine = create_engine(
    settings.database_url, 
    pool_size=settings.DB_POOL_SIZE, 
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DB_ECHO,
    pool_pre_ping=settings.POOL_PRE_PING
)


@contextmanager
def get_connection():
    try:
        with engine.connect() as connection:
            yield connection
    except OperationalError as connection_error:
        db_logger.error(f"Database Connection Error: {connection_error}")
        raise 


try:
    with get_connection() as connection:
        result = connection.execute(text('SELECT 1;'))
    print(result.scalar())
except Exception as error:
    db_logger.error(f"Error While : {error}")





