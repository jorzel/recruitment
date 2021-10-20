from abc import ABC, abstractmethod

from domain.entities.candidate import Candidate


class CandidateRepository(ABC):
    """
    Interface defining :class:`Candidate` storage
    """

    @abstractmethod
    def get(self, candidate_id: str):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def add(self, candidate: Candidate):
        pass
