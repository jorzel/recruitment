from sqlalchemy.orm import Session
from typing import Optional, Type

from domain.projections.store import ProjectionStore
from domain.projections.candidate import Projection
from domain.value_objects import AggregateId


class SQLAlchemyProjectionStore(ProjectionStore):
    def __init__(self, session: Session):
        self._session = session

    def get(
        self, projection_model: Type[Projection], aggregate_id: AggregateId
    ) -> Optional[Projection]:
        return self._session.query(projection_model).get(aggregate_id)

    def add(self, projection: Projection) -> None:
        self._session.add(projection)
        self._session.flush()
