import uuid
from typing import Any, Dict, List

from domain.events.base import DomainEvent
from domain.events.candidate import (
    AddedCandidate,
    InvitedCandidate,
    MovedToStandbyCandidate,
    RejectedCandidate,
)


class CandidateInvalidAction(Exception):
    pass


class UnrecognizedEvent(Exception):
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

    def __init__(self, events: List[DomainEvent], score_thresh: float = SCORE_THRESH):
        self.id = uuid.uuid1()
        self.SCORE_THRESH = score_thresh
        self.status: str
        self.score: float
        for event in events:
            self.apply(event)

    def apply(self, event: DomainEvent) -> DomainEvent:
        if isinstance(event, AddedCandidate):
            self._add(event)
        elif isinstance(event, InvitedCandidate):
            self._invite(event)
        elif isinstance(event, MovedToStandbyCandidate):
            self._move_to_standby(event)
        elif isinstance(event, RejectedCandidate):
            self._reject(event)
        else:
            raise UnrecognizedEvent()
        return event

    def add(self, profile: Dict[str, Any], score: float) -> AddedCandidate:
        return self.apply(
            AddedCandidate(candidate_id=self.id, profile=profile, score=score)
        )

    def _add(self, event: AddedCandidate):
        self.status = self.Status.ADDED
        self.score = event.score

    def invite(self) -> InvitedCandidate:
        return self.apply(InvitedCandidate(candidate_id=self.id))

    def _invite(self, event: InvitedCandidate):
        if self.status not in (self.Status.STANDBY, self.Status.ADDED):
            raise CandidateInvalidAction()
        if self.score < self.SCORE_THRESH:
            raise CandidateInvalidAction()
        self.status = self.Status.INVITED

    def move_to_standby(self) -> MovedToStandbyCandidate:
        return self.apply(MovedToStandbyCandidate(candidate_id=self.id))

    def _move_to_standby(self, event: MovedToStandbyCandidate):
        if self.status == self.Status.ADDED:
            self.status = self.Status.STANDBY
        else:
            raise CandidateInvalidAction()

    def reject(self) -> RejectedCandidate:
        return self.apply(RejectedCandidate(candidate_id=self.id))

    def _reject(self, event: RejectedCandidate):
        self.status = self.Status.REJECTED
