from abc import ABC, abstractmethod


class CandidateRepository(ABC):
    """
    Interface defining :class:`Candidate` storage
    """

    @abstractmethod
    def get(self, candidate_id):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def add(self, candidate):
        pass
