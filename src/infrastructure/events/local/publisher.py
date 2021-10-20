from typing import List

from application.events.handlers import handle_events
from application.events.publisher import EventPublisher
from domain.events.base import DomainEvent
from domain.repositories.candidate_projection import CandidateProjectionRepository
from infrastructure.events.local.handler import handlers


class LocalEventPublisher(EventPublisher):
    """
    Local implementation of publisher.

    It's not genuinely publish events to event bus, but it calls events handler
    """

    def __init__(self, candidate_projection_repository: CandidateProjectionRepository):
        self._candidate_projection_repository = candidate_projection_repository

    def publish(
        self,
        events: List[DomainEvent],
    ) -> None:
        handle_events(
            handlers,
            [e.as_dict for e in events],
            self._candidate_projection_repository,
        )
