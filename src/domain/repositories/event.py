from abc import ABC, abstractmethod
from typing import List

from domain.events.base import DomainEvent
from domain.value_objects import AggregateId


class EventRepository(ABC):
    """
    Interface defining :class:`DomainEvent` storage

    `originator_id` is id of aggregate that published event
    """

    @abstractmethod
    def filter_by_originator_id(self, originator_id: AggregateId) -> List[DomainEvent]:
        pass

    @abstractmethod
    def add(self, event: DomainEvent) -> None:
        pass
