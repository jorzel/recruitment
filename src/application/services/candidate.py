from typing import Any, Dict

from application.events.publisher import EventPublisher
from domain.entities.candidate import Candidate
from domain.repositories.candidate import CandidateRepository


class CandidateManagementService:
    def __init__(
        self, event_publisher: EventPublisher, candidate_repository: CandidateRepository
    ):
        self._event_publisher = event_publisher
        self._candidate_repository = candidate_repository

    def add(self, profile: Dict[str, Any], score: float) -> Candidate:
        candidate = Candidate()
        event = candidate.add(profile, score)
        self._candidate_repository.add(candidate)
        self._event_publisher.publish([event])
        return candidate

    def invite(self, candidate_id: str) -> None:
        candidate = self._candidate_repository.get(candidate_id)
        event = candidate.invite()
        self._event_publisher.publish([event])

    def move_to_standby(self, candidate_id: str) -> None:
        candidate = self._candidate_repository.get(candidate_id)
        event = candidate.move_to_standby()
        self._event_publisher.publish([event])

    def reject(self, candidate_id: str) -> None:
        candidate = self._candidate_repository.get(candidate_id)
        event = candidate.reject()
        self._event_publisher.publish([event])
