from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Float, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql.pypostgresql import PGDialect_pypostgresql
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite
from sqlalchemy.orm import mapper

from domain.projections.candidate import CandidateProjection
from domain.value_objects import AggregateId
from infrastructure.db.sqlalchemy.setup import engine, metadata


class StoredEvent:
    """
    Event representation for persistance
    """

    def __init__(
        self,
        originator_id: AggregateId,
        name: str,
        data: Dict[str, Any],
        timestamp: datetime,
    ):
        self.originator_id = originator_id
        self.data = data
        self.timestamp = timestamp
        self.name = name


dialects_json_type_mapper = {
    SQLiteDialect_pysqlite: JSON,
    PGDialect_pypostgresql: JSONB,
}

if isinstance(engine.dialect, SQLiteDialect_pysqlite):
    json_column_type = JSON
elif isinstance(engine.dialect, PGDialect_pypostgresql):
    json_column_type = JSONB
else:
    json_column_type = Text


events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("originator_id", String),
    Column("name", String),
    Column("data", json_column_type),
    Column("timestamp", DateTime),
)

candidate_projections = Table(
    "candidate_projections",
    metadata,
    Column("candidate_id", String, primary_key=True),
    Column("score", Float),
    Column("status", String),
    Column("profile", json_column_type),
    Column("added_at", DateTime),
    Column("invited_at", DateTime),
    Column("moved_to_standby_at", DateTime),
    Column("rejected_at", DateTime),
)


def run_mappers():
    """
    Provides mapping between db tables and domain models.
    """
    mapper(StoredEvent, events)
    mapper(
        CandidateProjection,
        candidate_projections,
    )
