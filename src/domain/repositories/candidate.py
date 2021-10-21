from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.candidate import Candidate


class CandidateRepository(ABC):
    """
    Interface defining :class:`Candidate` storage
    """

    @abstractmethod
    def get(self, candidate_id: str) -> Optional[Candidate]:
        pass

    @abstractmethod
    def save(self, candidate: Candidate) -> None:
        pass
