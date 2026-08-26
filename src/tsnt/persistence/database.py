"""Database construction kept separate for dependency injection."""

from collections.abc import Callable

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from tsnt.persistence.models import Base


def make_engine(database_url: str, echo: bool = False) -> Engine:
    return create_engine(database_url, echo=echo, pool_pre_ping=True)


def session_factory(engine: Engine) -> Callable[[], Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)


def create_schema(engine: Engine) -> None:
    Base.metadata.create_all(engine)
