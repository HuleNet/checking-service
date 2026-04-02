from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from checking_service.infrastructure.config.settings import get_settings


engine = create_async_engine(url=get_settings().db_url, echo=get_settings().db_echo)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
