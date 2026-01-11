from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column()
    isAdmin: Mapped[bool] = mapped_column()
    vakansion: Mapped[int] = mapped_column(nullable=True)
    name_surname: Mapped[str] = mapped_column(nullable=True)
    number: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    citizenship: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[str] = mapped_column(nullable=True)
    chatHistory: Mapped[str] = mapped_column(nullable=True)

class Jobs(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    jobType: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    secondDescription: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)