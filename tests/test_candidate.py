import pytest

from domain.entities.candidate import SCORE_THRESH, Candidate, CandidateInvalidAction


@pytest.fixture
def candidate_factory():
    def _candidate_factory(
        candidate_id, status=None, score=99.0, score_thresh=SCORE_THRESH
    ):
        candidate = Candidate(
            candidate_id, score=score, profile_id=1, score_thresh=score_thresh
        )
        if status:
            candidate.status = status
        return candidate

    return _candidate_factory


def test_candidate_move_to_standby(candidate_factory):
    candidate = candidate_factory(1, score=82.0)

    candidate.move_to_standby()

    assert candidate.status == Candidate.Status.STANDBY


def test_candidate_reject_when_already_invited(candidate_factory):
    candidate = candidate_factory(1, status=Candidate.Status.INVITED)

    candidate.reject()

    assert candidate.status == Candidate.Status.REJECTED


def test_candidate_invite_when_already_rejected_throw_exception(candidate_factory):
    candidate = candidate_factory(1, status=Candidate.Status.REJECTED)

    with pytest.raises(CandidateInvalidAction):
        candidate.invite()


def test_candidate_invite_when_score_below_thresh_throw_exception(candidate_factory):
    candidate = candidate_factory(1, score=78.0, score_thresh=80.0)
    with pytest.raises(CandidateInvalidAction):
        candidate.invite()


def test_candidate_invite_when_score_exceed_thresh(candidate_factory):
    candidate = candidate_factory(1, score=87.0, score_thresh=80.0)
    candidate.invite()

    assert candidate.status == Candidate.Status.INVITED
