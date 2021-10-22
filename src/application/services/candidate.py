import uuid
from typing import Any, Dict

from application.events.publisher import EventPublisher
from application.uow import UnitOfWork
from domain.entities.candidate import Candidate
from domain.repositories.candidate import CandidateRepository
from domain.value_objects import AggregateId


class CandidateManagementService:
    """
    Application service that handles incomming commands

    :meth:`EventPublisher.publish(events)` is called within :attr:`unit_of_work`
    context manager (within transcation if we use database). This implementation
    provides at least one delivery mechanism (event is dispatched, but
    transaction still can be rollbacked after that). So event handlers should be
    idempotent.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_publisher: EventPublisher,
        candidate_repository: CandidateRepository,
    ):
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher
        self._candidate_repository = candidate_repository

    def add(self, profile: Dict[str, Any], score: float) -> Candidate:
        with self._unit_of_work:
            candidate = Candidate(candidate_id=str(uuid.uuid1()), events=[])
            candidate.add(profile, score)
            self._candidate_repository.save(candidate)
            self._event_publisher.publish(candidate.changes)
            candidate.clear_changes()
            return candidate

    def invite(self, candidate_id: AggregateId) -> Candidate:
        with self._unit_of_work:
            candidate = self._candidate_repository.get(candidate_id)
            candidate.invite()
            self._candidate_repository.save(candidate)
            self._event_publisher.publish(candidate.changes)
            candidate.clear_changes()
            return candidate

    def move_to_standby(self, candidate_id: AggregateId) -> Candidate:
        with self._unit_of_work:
            candidate = self._candidate_repository.get(candidate_id)
            candidate.move_to_standby()
            self._candidate_repository.save(candidate)
            self._event_publisher.publish(candidate.changes)
            candidate.clear_changes()
            return candidate

    def reject(self, candidate_id: AggregateId) -> Candidate:
        with self._unit_of_work:
            candidate = self._candidate_repository.get(candidate_id)
            candidate.reject()
            self._candidate_repository.save(candidate)
            self._event_publisher.publish(candidate.changes)
            candidate.clear_changes()
            return candidate
