from dataclasses import asdict, dataclass
from typing import Any, Dict

SerializedEvent = Dict[str, Any]


@dataclass(frozen=True)
class DomainEvent:
    name = ""

    @property
    def as_dict(self) -> Dict:
        serialized = asdict(self)
        serialized["name"] = self.name
        return serialized
