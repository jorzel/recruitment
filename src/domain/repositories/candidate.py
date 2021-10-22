from typing import Optional

from domain.entities.candidate import Candidate
from domain.value_objects import AggregateId

from .event import EventRepository


class CandidateRepository:
    """
    Implementation for aggregate storage, based on events manipulations
    """

    def __init__(self, event_repository: EventRepository):
        self._event_repository = event_repository

    def get(self, candidate_id: AggregateId) -> Optional[Candidate]:
        events = self._event_repository.filter_by_originator_id(candidate_id)
        return Candidate(candidate_id, events)

    def save(self, candidate: Candidate) -> None:
        for event in candidate.changes:
            self._event_repository.add(event)
