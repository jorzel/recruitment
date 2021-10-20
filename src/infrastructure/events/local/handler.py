import logging

from domain.events.base import SerializedEvent
from domain.events.candidate import (
    AddedCandidateEvent,
    InvitedCandidateEvent,
    MovedToStandbyCandidateEvent,
    RejectedCandidateEvent,
)
from domain.projections.candidate import CandidateProjection
from domain.repositories.candidate_projection import CandidateProjectionRepository

logger = logging.getLogger(__name__)


class CandidateProjectionExist(Exception):
    pass


def handle_added_candidate(
    candidate_projection_repository: CandidateProjectionRepository,
    event: SerializedEvent,
):
    logger.info(f"Handling {event}")
    if candidate_projection_repository.get(event["candidate_id"]):
        raise CandidateProjectionExist()
    candidate_projection = CandidateProjection(event["candidate_id"])
    candidate_projection.handle_added(event)
    candidate_projection_repository.add(candidate_projection)


def handle_rejected_candidate(
    candidate_projection_repository: CandidateProjectionRepository,
    event: SerializedEvent,
) -> None:
    logger.info(f"Handling {event}")
    candidate_projection = candidate_projection_repository.get(event["candidate_id"])
    candidate_projection.handle_rejected(event)


def handle_moved_to_standby_candidate(
    candidate_projection_repository: CandidateProjectionRepository,
    event: SerializedEvent,
) -> None:
    logger.info(f"Handling {event}")
    candidate_projection = candidate_projection_repository.get(event["candidate_id"])
    candidate_projection.handle_moved_to_standby(event)


def handle_invited_candidate(
    candidate_projection_repository: CandidateProjectionRepository,
    event: SerializedEvent,
) -> None:
    logger.info(f"Handling {event}")
    candidate_projection = candidate_projection_repository.get(event["candidate_id"])
    candidate_projection.handle_invited(event)


handlers = {
    AddedCandidateEvent.name: handle_added_candidate,
    InvitedCandidateEvent.name: handle_invited_candidate,
    MovedToStandbyCandidateEvent.name: handle_moved_to_standby_candidate,
    RejectedCandidateEvent.name: handle_rejected_candidate,
}
