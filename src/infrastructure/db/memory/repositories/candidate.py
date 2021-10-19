from typing import List, Optional

from domain.entities.candidate import Candidate
from domain.repositories.candidate import CandidateRepository


class MemoryCandidateRepository(CandidateRepository):
    """
    In-memory implementation for :class:`Candidate` instances storage
    """

    def __init__(self):
        self._candidates = {}

    def get(self, candidate_id: int) -> Optional[Candidate]:
        return self._candidates.get(candidate_id)

    def all(self) -> List[Candidate]:
        return self._candidates.values()

    def add(self, candidate: Candidate) -> None:
        self._candidates[candidate.id] = candidate
