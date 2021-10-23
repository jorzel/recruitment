from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Table
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import mapper

from domain.projections.candidate import CandidateProjection
from domain.value_objects import AggregateId
from infrastructure.db.sqlalchemy.setup import metadata


class StoredEvent:
    """
    Event representation for persistance
    """

    def __init__(
        self, originator_id: AggregateId, name: str, data: str, timestamp: datetime
    ):
        self.originator_id = originator_id
        self.data = data
        self.timestamp = timestamp
        self.name = name


events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("originator_id", String),
    Column("name", String),
    Column("data", JSON),
    Column("timestamp", DateTime),
)

candidate_projections = Table(
    "candidate_projections",
    metadata,
    Column("candidate_id", String, primary_key=True),
    Column("score", Float),
    Column("status", String),
    Column("profile", JSON),
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
