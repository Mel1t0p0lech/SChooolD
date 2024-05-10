from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    user_id: Mapped[int]
    user_group: Mapped[int | None]
    created_at: Mapped[str]


class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[intpk]
    group_id: Mapped[str]
    title: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[str]


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    item: Mapped[int] = mapped_column(String(64))
    task: Mapped[str] = mapped_column(String(256))
    grade: Mapped[str] = mapped_column(String(6))
    group_id: Mapped[int]
    created_at: Mapped[str]


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)