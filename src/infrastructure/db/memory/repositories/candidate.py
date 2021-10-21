from typing import Optional

from domain.entities.candidate import Candidate
from domain.repositories.candidate import CandidateRepository

from .event import MemoryEventRepository


class MemoryCandidateRepository(CandidateRepository):
    """
    In-memory implementation for :class:`Candidate` instances storage
    """

    def __init__(self, event_repository: MemoryEventRepository):
        self._event_repository = event_repository

    def get(self, candidate_id: str) -> Optional[Candidate]:
        events = self._event_repository.filter_by_originator_id(candidate_id)
        return Candidate(candidate_id, events)

    def save(self, candidate: Candidate) -> None:
        for event in candidate.changes:
            self._event_repository.add(event)
        candidate.clear_changes()
