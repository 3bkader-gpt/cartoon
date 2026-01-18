from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class SourceEnum(str, enum.Enum):
    arabic_toons = "arabic_toons"
    egydead = "egydead"
    unknown = "unknown"


class JobTypeEnum(str, enum.Enum):
    fetch = "fetch"
    download = "download"
    export = "export"


class JobStatusEnum(str, enum.Enum):
    queued = "queued"
    running = "running"
    success = "success"
    error = "error"
    canceled = "canceled"


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[SourceEnum] = mapped_column(Enum(SourceEnum, name="source_enum"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    episodes: Mapped[list["Episode"]] = relationship(back_populates="series", cascade="all, delete-orphan")


class Episode(Base):
    __tablename__ = "episode"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    episode_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    size_hint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    series: Mapped[Series] = relationship(back_populates="episodes")


class Job(Base):
    __tablename__ = "job"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[JobTypeEnum] = mapped_column(Enum(JobTypeEnum, name="job_type_enum"), nullable=False)
    status: Mapped[JobStatusEnum] = mapped_column(Enum(JobStatusEnum, name="job_status_enum"), nullable=False, default=JobStatusEnum.queued)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
