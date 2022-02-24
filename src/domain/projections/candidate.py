from domain.events.base import SerializedEvent

from ..entities.candidate import Candidate


class Projection:
    pass


class CandidateProjection(Projection):
    """
    Read model that is build upon events dispatched by :class:`Candidate` aggregate
    """

    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id
        self.score = None
        self.status = None
        self.profile = None
        self.added_at = None
        self.invited_at = None
        self.rejected_at = None
        self.moved_to_standby_at = None

    def handle_added(self, event: SerializedEvent) -> None:
        self.status = Candidate.Status.ADDED
        self.score = event["score"]
        self.added_at = event["timestamp"]
        self.profile = event["profile"]

    def handle_rejected(self, event: SerializedEvent) -> None:
        self.status = Candidate.Status.REJECTED
        self.rejected_at = event["timestamp"]

    def handle_invited(self, event: SerializedEvent) -> None:
        self.status = Candidate.Status.INVITED
        self.invited_at = event["timestamp"]

    def handle_moved_to_standby(self, event: SerializedEvent) -> None:
        self.status = Candidate.Status.STANDBY
        self.moved_to_standby_at = event["timestamp"]
