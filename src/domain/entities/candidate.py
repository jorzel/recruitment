class CandidateInvalidAction(Exception):
    pass


SCORE_THRESH = 75.0


class Candidate:
    """
    Candidate is model representing person in first stage of recruitment process
    - Candidate is added to process at first.
    - Candidate can be invited to the next stage, only if score exceed X value
    - Candidate can be moved to standby list only if was not invited to the next stage
    - Candidate can be rejected at any time
    """

    class Status:
        ADDED = "ADDED"
        REJECTED = "REJECTED"
        STANDBY = "STANDBY"
        INVITED = "INVITED"  # invited for the next recruitment stage

    def __init__(
        self,
        candidate_id: int,
        score: float,
        profile_id: int,
        score_thresh: float = SCORE_THRESH,
    ):
        self.id = candidate_id
        self.SCORE_THRESH = score_thresh
        self.score = score
        self.profile_id = profile_id
        self.status = self.Status.ADDED

    def invite(self) -> None:
        if self.status not in (self.Status.STANDBY, self.Status.ADDED):
            raise CandidateInvalidAction()
        if self.score < self.SCORE_THRESH:
            raise CandidateInvalidAction()
        self.status = self.Status.INVITED

    def move_to_standby(self) -> None:
        if self.status == self.Status.ADDED:
            self.status = self.Status.STANDBY
        else:
            raise CandidateInvalidAction()

    def reject(self) -> None:
        self.status = self.Status.REJECTED
