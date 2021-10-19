import pytest

from domain.entities.candidate import SCORE_THRESH, Candidate, CandidateInvalidAction


@pytest.fixture
def candidate_factory():
    def _candidate_factory(
        status=None, profile=None, score=99.0, score_thresh=SCORE_THRESH
    ):
        candidate = Candidate(score_thresh=score_thresh)
        if not profile:
            profile = {"test": 1}
        if not status:
            status = Candidate.Status.ADDED
        candidate.status = status
        candidate.profile = profile
        candidate.score = score
        return candidate

    return _candidate_factory


def test_candidate_invite_when_already_rejected_throw_exception(candidate_factory):
    candidate = candidate_factory(status=Candidate.Status.REJECTED)

    with pytest.raises(CandidateInvalidAction):
        candidate.invite()


def test_candidate_invite_when_score_below_thresh_throw_exception(candidate_factory):
    candidate = candidate_factory(score=78.0, score_thresh=80.0)
    with pytest.raises(CandidateInvalidAction):
        candidate.invite()
