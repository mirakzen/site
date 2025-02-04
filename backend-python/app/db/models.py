from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.types import BIGINT, JSON

Base = declarative_base()


class Socials(Base):
    __tablename__ = "socials"

    id: Mapped[int] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column(nullable=False, unique=True)
    icon: Mapped[str] = mapped_column(nullable=False)


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    pictures: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    links: Mapped[list[dict[str, str | int]]] = mapped_column(JSON, nullable=True)


class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    subname: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column(nullable=True)
    picture: Mapped[str] = mapped_column(nullable=True)
    statuses: Mapped[list[dict[str, str]]] = mapped_column(JSON, nullable=False)
    full_completion: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)
    speenrun: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)
    genre: Mapped[str] = mapped_column(nullable=False)
    links: Mapped[list[dict[str, str | int]]] = mapped_column(JSON, nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)


class GamesStatuses(Base):
    __tablename__ = "games_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)
