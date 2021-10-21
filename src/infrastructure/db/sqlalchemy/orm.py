from sqlalchemy import Column, DateTime, Integer, String, Table, Text
from sqlalchemy.orm import mapper

from domain.events.base import Event
from infrastructure.db.sqlalchemy.setup import metadata

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
    mapper(Event, events)
