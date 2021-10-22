from abc import ABC, abstractmethod
from typing import Optional

from domain.projections.candidate import CandidateProjection
from domain.value_objects import AggregateId


class CandidateProjectionRepository(ABC):
    """
    Interface defining :class:`CandidateProjection` storage
    """

    @abstractmethod
    def get(self, candidate_id: AggregateId) -> Optional[CandidateProjection]:
        pass

    @abstractmethod
    def add(self, candidate_projection: CandidateProjection) -> None:
        pass
