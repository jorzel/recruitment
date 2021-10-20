import pytest

from domain.entities.candidate import Candidate, CandidateInvalidAction


def test_candidate_invite_when_already_rejected_throw_exception(candidate_factory):
    candidate = candidate_factory(status=Candidate.Status.REJECTED)
    with pytest.raises(CandidateInvalidAction):
        candidate.invite()


def test_candidate_invite_when_score_below_thresh_throw_exception(candidate_factory):
    candidate = candidate_factory(score=78.0, score_thresh=80.0)
    with pytest.raises(CandidateInvalidAction):
        candidate.invite()
