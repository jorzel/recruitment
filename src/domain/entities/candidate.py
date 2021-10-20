import uuid
from typing import Any, Dict

from domain.events.candidate import (
    AddedCandidateEvent,
    InvitedCandidateEvent,
    MovedToStandbyCandidateEvent,
    RejectedCandidateEvent,
)


class CandidateInvalidAction(Exception):
    pass


SCORE_THRESH = 75.0


class Candidate:
    """
    Candidate is an aggregate representing person in first stage of recruitment process
    - Candidate is added to process at first.
    - Candidate can be invited to the next stage, only if score exceed :attr:`score_thresh` value
    - Candidate can be moved to standby list only if was not invited to the next stage
    - Candidate can be rejected at any time
    """

    class Status:
        ADDED = "ADDED"
        REJECTED = "REJECTED"
        STANDBY = "STANDBY"
        INVITED = "INVITED"  # invited for the next recruitment stage

    def __init__(self, score_thresh: float = SCORE_THRESH):
        self.id = uuid.uuid1()
        self.SCORE_THRESH = score_thresh
        self.status: str
        self.score: float

    def add(self, profile: Dict[str, Any], score: float):
        self.status = self.Status.ADDED
        self.score = score
        return AddedCandidateEvent(candidate_id=self.id, profile=profile, score=score)

    def invite(self) -> None:
        if self.status not in (self.Status.STANDBY, self.Status.ADDED):
            raise CandidateInvalidAction()
        if self.score < self.SCORE_THRESH:
            raise CandidateInvalidAction()
        self.status = self.Status.INVITED
        return InvitedCandidateEvent(candidate_id=self.id)

    def move_to_standby(self) -> None:
        if self.status == self.Status.ADDED:
            self.status = self.Status.STANDBY
        else:
            raise CandidateInvalidAction()
        return MovedToStandbyCandidateEvent(candidate_id=self.id)

    def reject(self) -> None:
        self.status = self.Status.REJECTED
        return RejectedCandidateEvent(candidate_id=self.id)
