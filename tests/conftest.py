import pytest
from sqlalchemy.orm import sessionmaker

from domain.entities.candidate import SCORE_THRESH, Candidate
from infrastructure.db.sqlalchemy.setup import engine, metadata


@pytest.fixture
def candidate_factory():
    def _candidate_factory(
        status=None,
        profile=None,
        score=99.0,
        score_thresh=SCORE_THRESH,
        repository=None,
    ):
        candidate_id = "1222"
        if not profile:
            profile = {"test": 1}
        candidate = Candidate(
            candidate_id=candidate_id, events=[], score_thresh=score_thresh
        )
        if status == Candidate.Status.INVITED:
            candidate.add(profile=profile, score=score)
            candidate.invite()
        elif status == Candidate.Status.REJECTED:
            candidate.add(profile=profile, score=score)
            candidate.reject()
        elif status == Candidate.Status.STANDBY:
            candidate.add(profile=profile, score=score)
            candidate.move_to_standby()
        else:
            candidate.add(profile=profile, score=score)
        if repository:
            repository.save(candidate)
        return candidate

    return _candidate_factory


@pytest.fixture(scope="session")
def db_connection():
    metadata.drop_all()
    metadata.create_all()
    connection = engine.connect()

    yield connection

    metadata.drop_all()
    engine.dispose()


@pytest.fixture
def db_session(db_connection):
    transaction = db_connection.begin()
    session = sessionmaker(bind=db_connection)
    session = session()

    yield session

    transaction.rollback()
    session.close()
