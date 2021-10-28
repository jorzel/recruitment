import logging
from typing import Any, Dict, List

from application.uow import UnitOfWork
from domain.events.base import DomainEvent, SerializedEvent
from domain.events.candidate import (
    AddedCandidate,
    InvitedCandidate,
    MovedToStandbyCandidate,
    RejectedCandidate,
)
from domain.repositories.candidate_projection import CandidateProjectionRepository

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
        candidate_projection_repository: CandidateProjectionRepository,
    ):
        self._handlers = handlers
        self._unit_of_work = unit_of_work
        self._candidate_projection_repository = candidate_projection_repository

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

            if event["name"] not in (
                AddedCandidate.name,
                InvitedCandidate.name,
                RejectedCandidate.name,
                MovedToStandbyCandidate.name,
            ):
                logger.info(f"Cannot find repository for {event}")
                continue
            repository = self._candidate_projection_repository
            handler(self._unit_of_work, repository, event)
