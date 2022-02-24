import re
from typing import Optional, Type

from domain.projections.candidate import Projection
from domain.projections.store import ProjectionStore
from domain.value_objects import AggregateId


def camel_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class MemoryProjectionStore(ProjectionStore):
    """
    In-memory implementation for :class:`ProjectionStore` instances storage
    """

    def __init__(self):
        self._projections = {}

    def get(
        self, projection_model: Type[Projection], aggregate_id: AggregateId
    ) -> Optional[Projection]:
        model_name = projection_model.__name__
        return self._projections.get(model_name, {}).get(aggregate_id)

    def add(self, projection: Projection) -> None:
        model_name = projection.__class__.__name__
        if model_name not in self._projections:
            self._projections[model_name] = {}
        id_field = camel_to_snake(model_name) + "_id"
        self._projections[model_name][getattr(projection, id_field)] = projection
