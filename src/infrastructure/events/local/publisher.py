from typing import List

from application.events.handlers import EventHandler
from application.events.publisher import EventPublisher
from application.uow import UnitOfWork
from domain.events.base import DomainEvent
from domain.projections.store import ProjectionStore
from infrastructure.events.local.handler import handlers


class LocalEventPublisher(EventPublisher):
    """
    Local implementation of publisher.

    It's not genuinely publish events to event bus, but it calls events handler
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        projection_store: ProjectionStore,
    ):
        self._event_handler = EventHandler(handlers, unit_of_work, projection_store)

    def publish(
        self,
        events: List[DomainEvent],
    ) -> None:
        self._event_handler.handle([e.as_dict for e in events])
