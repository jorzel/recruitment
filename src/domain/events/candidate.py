from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from .base import DomainEvent


@dataclass(frozen=True)
class CandidateEvent(DomainEvent):
    candidate_id: str
    timestamp: datetime = datetime.utcnow()

    @property
    def name(self) -> str:
        return self.__class__.__name__


@dataclass(frozen=True)
class AddedCandidateEvent(DomainEvent):
    name = "AddedCandidateEvent"

    candidate_id: str
    profile: Dict[str, Any]
    score: float
    timestamp: datetime = datetime.utcnow()


class RejectedCandidateEvent(CandidateEvent):
    name = "RejectedCandidateEvent"


class MovedToStandbyCandidateEvent(CandidateEvent):
    name = "MovedToStandbyCandidateEvent"


class InvitedCandidateEvent(CandidateEvent):
    name = "InvitedCandidateEvent"
