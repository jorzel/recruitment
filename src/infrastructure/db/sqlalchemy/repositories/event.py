import json
from typing import List

import domain.events.candidate as domain_events
from domain.events.base import DomainEvent, Event
from domain.repositories.event import EventRepository

from ..orm import run_mappers

# temporary here, should be executed in app runtime
run_mappers()


class SQLAlchemyEventRepository(EventRepository):
    """
    SQLAlchemy db driver implementation of :class:`DomainEvent` storage
    """

    def __init__(self, session):
        self.session = session

    def filter_by_originator_id(self, originator_id: str) -> List[DomainEvent]:
        _events = []
        query = (
            self.session.query(Event)
            .filter_by(originator_id=originator_id)
            .order_by(Event.timestamp)
        )
        for event in query:
            event_class = getattr(domain_events, event.name)
            payload = json.loads(event.data)
            _events.append(event_class(**payload))
        return _events

    def add(self, event: DomainEvent) -> None:
        serialized_event = event.as_dict
        timestamp = serialized_event.pop("timestamp")
        name = serialized_event.pop("name")
        self.session.add(
            Event(
                originator_id=event.originator_id,
                name=name,
                timestamp=timestamp,
                data=json.dumps(serialized_event),
            )
        )
