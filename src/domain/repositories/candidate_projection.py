from abc import ABC, abstractmethod

from domain.projections.candidate import CandidateProjection


class CandidateProjectionRepository(ABC):
    """
    Interface defining :class:`CandidateProjection` storage
    """

    @abstractmethod
    def get(self, candidate_id: str):
        pass

    @abstractmethod
    def add(self, candidate_projection: CandidateProjection):
        pass
