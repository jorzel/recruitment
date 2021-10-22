from dataclasses import dataclass
from datetime import datetime

from .base import DomainEvent


@dataclass(frozen=True)
class CandidateEvent(DomainEvent):
    candidate_id: str
    timestamp: datetime = datetime.utcnow()

    @property
    def originator_id(self):
        return self.candidate_id


@dataclass(frozen=True)
class AddedCandidate(DomainEvent):
    name = "AddedCandidate"

    candidate_id: str
    profile: str  # stringfied json
    score: float
    timestamp: datetime = datetime.utcnow()

    @property
    def originator_id(self):
        return self.candidate_id


class RejectedCandidate(CandidateEvent):
    name = "RejectedCandidate"


class MovedToStandbyCandidate(CandidateEvent):
    name = "MovedToStandbyCandidate"


class InvitedCandidate(CandidateEvent):
    name = "InvitedCandidate"
