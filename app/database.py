import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


load_dotenv()

DB_USER_ROOT = os.getenv("DB_USER_ROOT")
DB_PASSWORD_ROOT = os.getenv("DB_PASSWORD_ROOT")
DB_USER_API = os.getenv("DB_USER_API")
DB_PASSWORD_API = os.getenv("DB_PASSWORD_API")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


DATABASE_URL_ROOT = f"postgresql+asyncpg://{DB_USER_ROOT}:{DB_PASSWORD_ROOT}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_URL_API = f"postgresql+asyncpg://{DB_USER_API}:{DB_PASSWORD_API}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL_API, echo=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)














