import logging
from typing import Any, Dict, List

from application.uow import UnitOfWork
from domain.events.base import DomainEvent, SerializedEvent
from domain.projections.store import ProjectionStore

logger = logging.getLogger(__name__)


class EventHandler:
    """
    `handlers` - is a key / value store, where key is :attr:`DomainEvent.name` and
                 value is callable defining what action should be made when the event is
                 handled
    """

    def __init__(
        self,
        handlers: Dict[DomainEvent, Any],
        unit_of_work: UnitOfWork,
        projection_store: ProjectionStore,
    ):
        self._handlers = handlers
        self._unit_of_work = unit_of_work
        self._projection_store = projection_store

    def handle(self, events: List[SerializedEvent]) -> None:
        """
        Method defining how incoming events are handled.
        `events` - list of serialized events
        """
        for event in events:
            handler = self._handlers.get(event["name"])
            if not handler:
                logger.info(f"Handler for {event} not found")
                continue
            handler(self._unit_of_work, self._projection_store, event)
