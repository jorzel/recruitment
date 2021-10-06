from src.domain.entities.candidate import Candidate


def test_candidate_move_to_standby_succesful():
    candidate = Candidate(score=82.0, profile_id=1)

    candidate.move_to_standby()

    assert candidate.status == Candidate.Status.STANDBY
