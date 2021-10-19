from typing import Optional

from domain.projections.candidate import CandidateProjection
from domain.repositories.candidate_projection import CandidateProjectionRepository


class MemoryCandidateProjectionRepository(CandidateProjectionRepository):
    """
    In-memory implementation for :class:`CandidateProjection` instances storage
    """

    def __init__(self):
        self._projections = {}

    def get(self, candidate_id: int) -> Optional[CandidateProjection]:
        return self._projections.get(candidate_id)

    def add(self, candidate_projection: CandidateProjection) -> None:
        self._projections[candidate_projection.candidate_id] = candidate_projection
