import uuid
from typing import Any, Dict

from domain.events.base import DomainEvent
from domain.events.candidate import (
    AddedCandidateEvent,
    InvitedCandidateEvent,
    MovedToStandbyCandidateEvent,
    RejectedCandidateEvent,
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

    def __init__(self, score_thresh: float = SCORE_THRESH):
        self.id = uuid.uuid1()
        self.SCORE_THRESH = score_thresh
        self.status: str
        self.score: float

    def apply(self, event: DomainEvent):
        if isinstance(event, AddedCandidateEvent):
            self._add(event)
        elif isinstance(event, InvitedCandidateEvent):
            self._invite(event)
        elif isinstance(event, MovedToStandbyCandidateEvent):
            self._move_to_standby(event)
        elif isinstance(event, RejectedCandidateEvent):
            self._reject(event)
        else:
            raise UnrecognizedEvent()
        return event

    def add(self, profile: Dict[str, Any], score: float):
        return self.apply(
            AddedCandidateEvent(candidate_id=self.id, profile=profile, score=score)
        )

    def _add(self, event: AddedCandidateEvent):
        self.status = self.Status.ADDED
        self.score = event.score

    def invite(self) -> None:
        return self.apply(InvitedCandidateEvent(candidate_id=self.id))

    def _invite(self, event: InvitedCandidateEvent):
        if self.status not in (self.Status.STANDBY, self.Status.ADDED):
            raise CandidateInvalidAction()
        if self.score < self.SCORE_THRESH:
            raise CandidateInvalidAction()
        self.status = self.Status.INVITED

    def move_to_standby(self) -> None:
        return self.apply(MovedToStandbyCandidateEvent(candidate_id=self.id))

    def _move_to_standby(self, event: MovedToStandbyCandidateEvent):
        if self.status == self.Status.ADDED:
            self.status = self.Status.STANDBY
        else:
            raise CandidateInvalidAction()

    def reject(self) -> None:
        return self.apply(RejectedCandidateEvent(candidate_id=self.id))

    def _reject(self, event: RejectedCandidateEvent):
        self.status = self.Status.REJECTED
