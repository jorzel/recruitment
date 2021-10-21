import pytest

from domain.entities.candidate import SCORE_THRESH, Candidate


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
