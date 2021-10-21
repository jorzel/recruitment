import logging
from typing import Any, Dict, List

from domain.events.base import DomainEvent, SerializedEvent
from domain.events.candidate import (
    AddedCandidate,
    InvitedCandidate,
    MovedToStandbyCandidate,
    RejectedCandidate,
)
from domain.repositories.candidate_projection import CandidateProjectionRepository

logger = logging.getLogger(__name__)


def handle_events(
    handlers: Dict[DomainEvent, Any],
    events: List[SerializedEvent],
    candidate_projection_repository: CandidateProjectionRepository,
) -> None:
    """
    Method defining how incoming events are handled.
    `handlers` - is a key / value store, where key is :attr:`DomainEvent.name` and
                 value is callable defining what action should be made when the event is
                 handled
    `events` - list of serialized events
    """
    for event in events:
        handler = handlers.get(event["name"])
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
        repository = candidate_projection_repository
        handler(repository, event)
