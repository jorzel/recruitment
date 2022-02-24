import logging

from application.uow import UnitOfWork
from domain.events.base import SerializedEvent
from domain.events.candidate import (
    AddedCandidate,
    InvitedCandidate,
    MovedToStandbyCandidate,
    RejectedCandidate,
)
from domain.projections.candidate import CandidateProjection
from domain.projections.store import ProjectionStore

logger = logging.getLogger(__name__)


class CandidateProjectionExist(Exception):
    pass


def handle_added_candidate(
    unit_of_work: UnitOfWork,
    projection_store: ProjectionStore,
    event: SerializedEvent,
):
    logger.info(f"Handling {event}")
    with unit_of_work:
        if projection_store.get(CandidateProjection, event["candidate_id"]):
            raise CandidateProjectionExist()
        candidate_projection = CandidateProjection(event["candidate_id"])
        candidate_projection.handle_added(event)
        projection_store.add(candidate_projection)


def handle_rejected_candidate(
    unit_of_work: UnitOfWork,
    projection_store: ProjectionStore,
    event: SerializedEvent,
) -> None:
    logger.info(f"Handling {event}")
    with unit_of_work:
        candidate_projection = projection_store.get(
            CandidateProjection, event["candidate_id"]
        )
        candidate_projection.handle_rejected(event)


def handle_moved_to_standby_candidate(
    unit_of_work: UnitOfWork,
    projection_store: ProjectionStore,
    event: SerializedEvent,
) -> None:
    logger.info(f"Handling {event}")
    with unit_of_work:
        candidate_projection = projection_store.get(
            CandidateProjection, event["candidate_id"]
        )
        candidate_projection.handle_moved_to_standby(event)


def handle_invited_candidate(
    unit_of_work: UnitOfWork,
    projection_store: ProjectionStore,
    event: SerializedEvent,
) -> None:
    logger.info(f"Handling {event}")
    with unit_of_work:
        candidate_projection = projection_store.get(
            CandidateProjection, event["candidate_id"]
        )
        candidate_projection.handle_invited(event)


handlers = {
    AddedCandidate.name: handle_added_candidate,
    InvitedCandidate.name: handle_invited_candidate,
    MovedToStandbyCandidate.name: handle_moved_to_standby_candidate,
    RejectedCandidate.name: handle_rejected_candidate,
}
