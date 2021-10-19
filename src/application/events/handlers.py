import logging
from typing import Any, Dict, List

from domain.events.base import DomainEvent
from domain.events.candidate import (
    AddedCandidateEvent,
    InvitedCandidateEvent,
    MovedToStandbyCandidateEvent,
    RejectedCandidateEvent,
)
from domain.repositories.candidate_projection import CandidateProjectionRepository

logger = logging.getLogger(__name__)


def handle_events(
    handlers: Dict[DomainEvent, Any],
    candidate_projection_repository: CandidateProjectionRepository,
    events: List[Dict[str, Any]],
) -> List[str]:
    """
    Primary port defining how incoming events are handled.
    `handlers` - is a key / value store, where key is :attr:`DomainEvent.name` and
                 value is callable defining what action should be made when the event is
                 handled
    `events` - list of serialized events
    """
    handled = []
    for event in events:
        handler = handlers.get(event["name"])
        if not handler:
            logger.info(f"Handler for {event} not found")
            continue
        if event["name"] not in (
            AddedCandidateEvent.name,
            InvitedCandidateEvent.name,
            RejectedCandidateEvent.name,
            MovedToStandbyCandidateEvent.name,
        ):
            logger.info(f"Cannot find repository for {event}")
            continue
        repository = candidate_projection_repository
        handled.append(handler(repository, event))
    return handled
