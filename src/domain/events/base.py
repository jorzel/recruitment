from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict

SerializedEvent = Dict[str, Any]


@dataclass(frozen=True)
class DomainEvent:
    name = ""

    @property
    def originator_id(self):
        raise NotImplementedError()

    @property
    def as_dict(self) -> Dict:
        serialized = asdict(self)
        serialized["name"] = self.name
        return serialized


class Event:
    """
    Event representation for persistance
    """

    def __init__(self, originator_id: str, name: str, data: str, timestamp: datetime):
        self.originator_id = originator_id
        self.data = data
        self.timestamp = timestamp
        self.name = name
