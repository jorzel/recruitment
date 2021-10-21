from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from .base import DomainEvent


@dataclass(frozen=True)
class CandidateEvent(DomainEvent):
    candidate_id: str
    timestamp: datetime = datetime.utcnow()


@dataclass(frozen=True)
class AddedCandidate(DomainEvent):
    name = "AddedCandidate"

    candidate_id: str
    profile: Dict[str, Any]
    score: float
    timestamp: datetime = datetime.utcnow()


class RejectedCandidate(CandidateEvent):
    name = "RejectedCandidate"


class MovedToStandbyCandidate(CandidateEvent):
    name = "MovedToStandbyCandidate"


class InvitedCandidate(CandidateEvent):
    name = "InvitedCandidate"
