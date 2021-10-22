from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Table, Text
from sqlalchemy.orm import mapper

from infrastructure.db.sqlalchemy.setup import metadata


class StoredEvent:
    """
    Event representation for persistance
    """

    def __init__(self, originator_id: str, name: str, data: str, timestamp: datetime):
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
    Column("data", Text),
    Column("timestamp", DateTime),
)


def run_mappers():
    """
    Provides mapping between db tables and domain models.
    """
    mapper(StoredEvent, events)
