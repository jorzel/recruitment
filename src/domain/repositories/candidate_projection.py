from abc import ABC, abstractmethod


class CandidateProjectionRepository(ABC):
    """
    Interface defining :class:`CandidateProjection` storage
    """

    @abstractmethod
    def get(self, candidate_id):
        pass

    @abstractmethod
    def add(self, candidate_projection):
        pass
