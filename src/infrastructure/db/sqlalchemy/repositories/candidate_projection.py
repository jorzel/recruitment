from typing import Optional

from sqlalchemy.orm import Session

from domain.projections.candidate import CandidateProjection
from domain.repositories.candidate_projection import CandidateProjectionRepository


class SQLAlchemyCandidateProjectionRepository(CandidateProjectionRepository):
    """
    SQLAlchemy implementation for :class:`CandidateProjection` instances storage
    """

    def __init__(self, session: Session):
        self.session = session

    @property
    def queryset(self):
        return self.session.query(CandidateProjection)

    def get(self, candidate_id: int) -> Optional[CandidateProjection]:
        return self.queryset.get(candidate_id)

    def add(self, candidate_projection: CandidateProjection) -> None:
        self.session.add(candidate_projection)
        self.session.flush()
