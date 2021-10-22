import uuid
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
        candidate = Candidate(candidate_id=str(uuid.uuid1()), events=[])
        candidate.add(profile, score)
        self._candidate_repository.save(candidate)
        self._event_publisher.publish(candidate.changes)
        candidate.clear_changes()
        return candidate

    def invite(self, candidate_id: str) -> Candidate:
        candidate = self._candidate_repository.get(candidate_id)
        candidate.invite()
        self._candidate_repository.save(candidate)
        self._event_publisher.publish(candidate.changes)
        candidate.clear_changes()
        return candidate

    def move_to_standby(self, candidate_id: str) -> Candidate:
        candidate = self._candidate_repository.get(candidate_id)
        candidate.move_to_standby()
        self._candidate_repository.save(candidate)
        self._event_publisher.publish(candidate.changes)
        candidate.clear_changes()
        return candidate

    def reject(self, candidate_id: str) -> Candidate:
        candidate = self._candidate_repository.get(candidate_id)
        candidate.reject()
        self._candidate_repository.save(candidate)
        self._event_publisher.publish(candidate.changes)
        candidate.clear_changes()
        return candidate
