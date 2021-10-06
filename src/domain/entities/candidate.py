class Candidate:
    """
    Candidate is model representing person in first stage of recruitment process
    - Candidate is added to process at first.
    - Candidate can be invited to the next stage, only if score exceed X value
    - Candidate can be moved to standby list only if was not invited to the next stage
    - Candidate can be rejected only if was not invited to the next stage
    """

    class Status:
        ADDED = "ADDED"
        REJECTED = "REJECTED"
        STANDBY = "STANDBY"
        INVITED = "INVITED"  # invited for the next recruitment stage

    def __init__(self, score: float, profile_id: int):
        self.score = score
        self.profile_id = profile_id
        self.status = self.Status.ADDED

    def move_to_standby(self) -> None:
        if self.status in (self.Status.ADDED, self.Status.REJECTED):
            self.status = self.Status.STANDBY
