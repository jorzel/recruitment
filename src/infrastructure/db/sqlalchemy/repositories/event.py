from typing import List

from sqlalchemy.orm import Session

import domain.events.candidate as domain_events
from domain.events.base import DomainEvent
from domain.repositories.event import EventRepository
from domain.value_objects import AggregateId
from infrastructure.db.sqlalchemy.orm import StoredEvent, run_mappers

# temporary here, should be executed in app runtime
run_mappers()


class EventMapper:
    """
    Bidirectional event mapper that provide transformations:
    - encode: DomainEvent -> StorageEvent
    - decode: StarageEvent -> DomainEvent
    """

    def encode(self, domain_event: DomainEvent) -> StoredEvent:
        serialized_event = domain_event.as_dict
        timestamp = serialized_event.pop("timestamp")
        name = serialized_event.pop("name")
        return StoredEvent(
            originator_id=domain_event.originator_id,
            name=name,
            timestamp=timestamp,
            data=serialized_event,
        )

    def decode(self, stored_event: StoredEvent) -> DomainEvent:
        domain_event_class = getattr(domain_events, stored_event.name)
        payload = stored_event.data
        payload["timestamp"] = stored_event.timestamp
        return domain_event_class(**payload)


class SQLAlchemyEventRepository(EventRepository):
    """
    SQLAlchemy db driver implementation of :class:`DomainEvent` storage
    """

    def __init__(self, session: Session):
        self._session = session
        self._event_mapper = EventMapper()

    def filter_by_originator_id(self, originator_id: AggregateId) -> List[DomainEvent]:
        _events = []
        query = (
            self._session.query(StoredEvent)
            .filter_by(originator_id=originator_id)
            .order_by(StoredEvent.timestamp)
        )
        for stored_event in query:
            domain_event = self._event_mapper.decode(stored_event)
            _events.append(domain_event)
        return _events

    def add(self, domain_event: DomainEvent) -> None:
        stored_event = self._event_mapper.encode(domain_event)
        self._session.add(stored_event)
        self._session.flush()
