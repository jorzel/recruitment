from abc import ABC, abstractmethod
from typing import Optional, Type

from domain.projections.candidate import Projection
from domain.value_objects import AggregateId


class ProjectionStore:
    """
    Interface defining :class:`Projection` storage
    """

    @abstractmethod
    def get(
        self, projection_model: Type[Projection], aggregate_id: AggregateId
    ) -> Optional[Projection]:
        pass

    @abstractmethod
    def add(self, projection: Projection) -> None:
        pass
