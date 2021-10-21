from abc import ABC, abstractmethod
from typing import List

from domain.events.base import DomainEvent


class EventRepository(ABC):
    """
    Interface defining :class:`DomainEvent` storage

    `originator_id` is id of aggregate that published event
    """

    @abstractmethod
    def filter_by_originator_id(self, originator_id: str) -> List[DomainEvent]:
        pass

    @abstractmethod
    def add(self, event: DomainEvent) -> None:
        pass
