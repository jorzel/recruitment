from typing import List

from domain.events.base import DomainEvent
from domain.repositories.event import EventRepository


class MemoryEventRepository(EventRepository):
    """
    In-memory implementation of :class:`DomainEvent` storage
    """

    def __init__(self):
        self._events = {}

    def filter_by_originator_id(self, originator_id: str) -> List[DomainEvent]:
        return self._events.get(originator_id, [])

    def add(self, event: DomainEvent) -> None:
        if event.originator_id not in self._events:
            self._events[event.originator_id] = []
        self._events[event.originator_id].append(event)
