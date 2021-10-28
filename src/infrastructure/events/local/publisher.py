from typing import List

from application.events.handlers import EventHandler
from application.events.publisher import EventPublisher
from application.uow import UnitOfWork
from domain.events.base import DomainEvent
from domain.repositories.candidate_projection import CandidateProjectionRepository
from infrastructure.events.local.handler import handlers


class LocalEventPublisher(EventPublisher):
    """
    Local implementation of publisher.

    It's not genuinely publish events to event bus, but it calls events handler
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        candidate_projection_repository: CandidateProjectionRepository,
    ):
        self._event_handler = EventHandler(
            handlers, unit_of_work, candidate_projection_repository
        )

    def publish(
        self,
        events: List[DomainEvent],
    ) -> None:
        self._event_handler.handle([e.as_dict for e in events])
