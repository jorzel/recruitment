import pytest

from application.services.candidate import CandidateManagementService
from domain.entities.candidate import SCORE_THRESH, Candidate
from domain.projections.candidate import CandidateProjection
from infrastructure.db.memory.repositories.candidate import MemoryCandidateRepository
from infrastructure.db.memory.repositories.candidate_projection import (
    MemoryCandidateProjectionRepository,
)
from infrastructure.events.local.publisher import LocalEventPublisher


@pytest.fixture
def candidate_projection_factory():
    def _candidate_projection_factory(repository, candidate_id):
        projection = CandidateProjection(candidate_id)
        repository.add(projection)
        return projection

    return _candidate_projection_factory


@pytest.fixture
def candidate_factory():
    def _candidate_factory(
        repository, status=None, profile=None, score=90.0, score_thresh=SCORE_THRESH
    ):
        if not profile:
            profile = {"test": 1}
        candidate = Candidate(score_thresh=score_thresh)
        if not status:
            status = Candidate.Status.ADDED
        candidate.status = status
        candidate.profile = profile
        candidate.score = score
        repository.add(candidate)
        return candidate

    return _candidate_factory


def test_candidate_management_add():
    candidate_repository = MemoryCandidateRepository()
    candidate_projection_repository = MemoryCandidateProjectionRepository()
    event_publisher = LocalEventPublisher(candidate_projection_repository)
    candidate_service = CandidateManagementService(
        event_publisher=event_publisher, candidate_repository=candidate_repository
    )
    score = 88.0
    profile = {"test": 1}

    candidate = candidate_service.add(profile=profile, score=score)

    projection = candidate_projection_repository.get(candidate.id)
    assert candidate.status == Candidate.Status.ADDED
    assert candidate.score == score
    assert projection.status == Candidate.Status.ADDED
    assert projection.added_at is not None
    assert projection.score == score
    assert projection.profile == profile


def test_candidate_management_move_to_standby(
    candidate_factory, candidate_projection_factory
):
    candidate_repository = MemoryCandidateRepository()
    candidate_projection_repository = MemoryCandidateProjectionRepository()
    event_publisher = LocalEventPublisher(candidate_projection_repository)
    candidate = candidate_factory(candidate_repository)
    projection = candidate_projection_factory(
        candidate_projection_repository, candidate.id
    )
    candidate_service = CandidateManagementService(
        event_publisher=event_publisher, candidate_repository=candidate_repository
    )

    candidate_service.move_to_standby(candidate.id)

    assert candidate.status == Candidate.Status.STANDBY
    assert projection.status == Candidate.Status.STANDBY
    assert projection.moved_to_standby_at is not None


def test_candidate_management_reject(candidate_factory, candidate_projection_factory):
    candidate_repository = MemoryCandidateRepository()
    candidate_projection_repository = MemoryCandidateProjectionRepository()
    event_publisher = LocalEventPublisher(candidate_projection_repository)
    candidate = candidate_factory(candidate_repository, status=Candidate.Status.ADDED)
    projection = candidate_projection_factory(
        candidate_projection_repository, candidate.id
    )
    candidate_service = CandidateManagementService(
        event_publisher=event_publisher, candidate_repository=candidate_repository
    )

    candidate_service.reject(candidate.id)

    assert candidate.status == Candidate.Status.REJECTED
    assert projection.status == Candidate.Status.REJECTED
    assert projection.rejected_at is not None


def test_candidate_invite_when_score_exceed_thresh(
    candidate_factory, candidate_projection_factory
):
    candidate_repository = MemoryCandidateRepository()
    candidate_projection_repository = MemoryCandidateProjectionRepository()
    event_publisher = LocalEventPublisher(candidate_projection_repository)
    candidate = candidate_factory(candidate_repository)
    projection = candidate_projection_factory(
        candidate_projection_repository, candidate.id
    )
    candidate_service = CandidateManagementService(
        event_publisher=event_publisher, candidate_repository=candidate_repository
    )

    candidate_service.invite(candidate.id)

    assert candidate.status == Candidate.Status.INVITED
    assert projection.status == Candidate.Status.INVITED
    assert projection.invited_at is not None
