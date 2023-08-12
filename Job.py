import datetime


class Job:
    def __init__(
        self,
        id: int,
        dateApplied: str,
        company: str,
        position: str,
        jobBoard: str,
        website: str,
        resume: str,
        coverLetter: str,
        statusList: str,
    ):
        self.id: int = id
        self.dateApplied: datetime.date = self._parse_date_applied(dateApplied)
        self.company: str = company
        self.position: str = position
        self.jobBoard: str = jobBoard
        self.website: str = website
        self.resume: str = resume
        self.coverLetter: str = coverLetter
        self.statusList: list[str] = self._parse_status_list(statusList)

    ## helper methods

    def _parse_date_applied(self, dateApplied: str) -> datetime.date:
        return datetime.datetime.strptime(dateApplied, "%Y-%m-%d").date()

    def _parse_status_list(self, statusList: str) -> list[str]:
        return statusList.split(">")
