from abc import ABC, abstractmethod


class EventPublisher(ABC):
    """
    Interface for event dispatchers
    """

    @abstractmethod
    def publish(self, events):
        pass
