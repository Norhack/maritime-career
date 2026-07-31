import logging
import os
from collections.abc import AsyncGenerator, Generator
from urllib.parse import urlsplit, urlunsplit

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)


def redact_database_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return url

    if not parsed.password:
        return url

    userinfo = parsed.username or ""
    if parsed.username and parsed.password:
        userinfo = f"{parsed.username}:***"
    elif parsed.password:
        userinfo = "***"

    netloc = userinfo
    if parsed.hostname:
        netloc = f"{userinfo}@{parsed.hostname}" if userinfo else parsed.hostname
        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"

    return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./maritime_career.db")

engine_options: dict[str, object] = {}
if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Database engine initialized with URL: %s", redact_database_url(DATABASE_URL))

# Async setup
async_database_url = DATABASE_URL
if DATABASE_URL.startswith("sqlite"):
    async_database_url = "sqlite+aiosqlite:///" + DATABASE_URL.split("sqlite:///")[-1]

async_engine = create_async_engine(
    async_database_url, 
    echo=False,
    pool_pre_ping=True
)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
logger.info("Async database engine initialized with URL: %s", redact_database_url(async_database_url))


def get_db() -> Generator[Session, None, None]:
    logger.debug("Creating new database session")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error during database session: {e}", exc_info=True)
        raise
    finally:
        db.close()
        logger.debug("Database session closed")


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Creating new async database session")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Error during async database session: {e}", exc_info=True)
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            logger.debug("Async database session closed")
