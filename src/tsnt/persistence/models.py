"""SQLAlchemy tables for versioned inputs and immutable run manifests."""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class NodeVersion(Base):
    __tablename__ = "node_versions"

    version_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    node_id: Mapped[str] = mapped_column(String(200), index=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    transaction_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class EdgeVersion(Base):
    __tablename__ = "edge_versions"

    version_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    edge_id: Mapped[str] = mapped_column(String(200), index=True)
    source: Mapped[str] = mapped_column(String(200), index=True)
    target: Mapped[str] = mapped_column(String(200), index=True)
    capacity: Mapped[float] = mapped_column(Float)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    transaction_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class ScenarioRun(Base):
    __tablename__ = "scenario_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scenario_id: Mapped[str] = mapped_column(String(200), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    code_version: Mapped[str] = mapped_column(String(80))
    input_manifest_hash: Mapped[str] = mapped_column(String(64), index=True)
    request_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    result_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    notes: Mapped[str | None] = mapped_column(Text)
