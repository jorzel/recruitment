import pytest

from application.services.candidate import CandidateManagementService
from domain.entities.candidate import Candidate
from domain.projections.candidate import CandidateProjection
from domain.repositories.candidate import CandidateRepository
from infrastructure.db.sqlalchemy.projections import SQLAlchemyProjectionStore
from infrastructure.db.sqlalchemy.repositories.event import SQLAlchemyEventRepository
from infrastructure.db.sqlalchemy.uow import SQLAlchemyUnitOfWork
from infrastructure.events.local.publisher import LocalEventPublisher


@pytest.fixture
def unit_of_work(db_session):
    return SQLAlchemyUnitOfWork(db_session)


@pytest.fixture
def event_repository(db_session):
    return SQLAlchemyEventRepository(db_session)


@pytest.fixture
def candidate_repository(event_repository):
    return CandidateRepository(event_repository)


@pytest.fixture
def projection_store(db_session):
    return SQLAlchemyProjectionStore(db_session)


@pytest.fixture
def event_publisher(projection_store, unit_of_work):
    return LocalEventPublisher(unit_of_work, projection_store)


@pytest.fixture
def candidate_service(unit_of_work, event_publisher, candidate_repository):
    return CandidateManagementService(
        unit_of_work, event_publisher, candidate_repository
    )


@pytest.fixture
def candidate_projection_factory():
    def _candidate_projection_factory(store, candidate_id):
        projection = CandidateProjection(candidate_id)
        store.add(projection)
        return projection

    return _candidate_projection_factory


def test_candidate_management_add(candidate_service, projection_store):
    score = 88.0
    profile = {"test": 1}

    candidate = candidate_service.add(profile=profile, score=score)

    projection = projection_store.get(CandidateProjection, candidate.id)
    assert candidate.status == Candidate.Status.ADDED
    assert candidate.score == score
    assert projection.status == Candidate.Status.ADDED
    assert projection.added_at is not None
    assert projection.score == score
    assert projection.profile == profile


def test_candidate_management_move_to_standby(
    candidate_factory,
    candidate_projection_factory,
    candidate_service,
    candidate_repository,
    projection_store,
):
    candidate = candidate_factory(repository=candidate_repository)
    projection = candidate_projection_factory(projection_store, candidate.id)

    candidate = candidate_service.move_to_standby(candidate.id)
    assert candidate.status == Candidate.Status.STANDBY
    assert projection.status == Candidate.Status.STANDBY
    assert projection.moved_to_standby_at is not None


def test_candidate_management_reject(
    candidate_factory,
    candidate_projection_factory,
    candidate_service,
    candidate_repository,
    projection_store,
):
    candidate = candidate_factory(repository=candidate_repository)
    projection = candidate_projection_factory(projection_store, candidate.id)

    candidate = candidate_service.reject(candidate.id)

    assert candidate.status == Candidate.Status.REJECTED
    assert projection.status == Candidate.Status.REJECTED
    assert projection.rejected_at is not None


def test_candidate_invite_when_score_exceed_thresh(
    candidate_factory,
    candidate_projection_factory,
    candidate_service,
    candidate_repository,
    projection_store,
):
    candidate = candidate_factory(repository=candidate_repository)
    projection = candidate_projection_factory(projection_store, candidate.id)

    candidate = candidate_service.invite(candidate.id)

    assert candidate.status == Candidate.Status.INVITED
    assert projection.status == Candidate.Status.INVITED
    assert projection.invited_at is not None
