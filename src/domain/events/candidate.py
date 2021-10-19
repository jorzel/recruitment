from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from .base import DomainEvent


@dataclass(frozen=True)
class CandidateEvent(DomainEvent):
    candidate_id: int
    timestamp: datetime = datetime.utcnow()


@dataclass(frozen=True)
class AddedCandidateEvent(DomainEvent):
    name = "added_candidate"
    candidate_id: int
    profile: Dict[str, Any]
    score: float
    timestamp: datetime = datetime.utcnow()


class RejectedCandidateEvent(CandidateEvent):
    name = "rejected_candidate"


class MovedToStandbyCandidateEvent(CandidateEvent):
    name = "moved_to_standby_candidate"


class InvitedCandidateEvent(CandidateEvent):
    name = "invited_candidate"
