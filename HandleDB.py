import csv
import shutil
from Job import Job
from pathlib import Path


class HandleDB:
    def __init__(self, db_path: str = "./db/"):
        self._data_path: str = db_path + "data.csv"
        self._jobs: list[Job] = self._load_jobs()

    # helper methods

    def _load_jobs(self) -> list[Job]:
        jobs: list[Job] = []

        with open(self._data_path, "r") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                jobs.append(
                    Job(
                        id=int(row[0]),
                        dateApplied=row[1],
                        company=row[2],
                        position=row[3],
                        jobBoard=row[4],
                        website=row[5],
                        resume=row[6],
                        coverLetter=row[7],
                        statusList=row[8],
                    )
                )

        return jobs

    def _write_jobs(self) -> None:
        with open(self._data_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "id",
                    "dateApplied",
                    "company",
                    "position",
                    "jobBoard",
                    "website",
                    "resume",
                    "coverLetter",
                    "statusList",
                ]
            )

            for job in self._jobs:
                writer.writerow(
                    [
                        job.id,
                        job.dateApplied,
                        job.company,
                        job.position,
                        job.jobBoard,
                        job.website,
                        job.resume,
                        job.coverLetter,
                        ">".join(job.statusList),
                    ]
                )

    # public methods

    def get_jobs(self) -> list[Job]:
        return self._jobs

    def get_job(self, id: int) -> Job:
        for job in self._jobs:
            if job.id == id:
                return job

        raise Exception("Job not found")

    def add_job(self, job: Job) -> None:
        job.id = len(self._jobs) + 1
        self._jobs.append(job)

        self.add_file(job.id, Path(job.resume), "resume")
        self.add_file(job.id, Path(job.coverLetter), "coverLetter")

        self._write_jobs()

    def update_job(self, job: Job) -> None:
        for i, j in enumerate(self._jobs):
            if j.id == job.id:
                self._jobs[i] = job
                self._write_jobs()
                return

        raise Exception("Job not found")

    def delete_job(self, id: int) -> None:
        for i, job in enumerate(self._jobs):
            if job.id == id:
                # delete files from db
                if job.resume != "":
                    Path(job.resume).unlink()
                if job.coverLetter != "":
                    Path(job.coverLetter).unlink()

                self._jobs.pop(i)
                for i, job in enumerate(self._jobs):
                    job.id = i + 1
                self._write_jobs()
                return

        raise Exception("Job not found")
    
    def add_file(self, id: int, file: Path, type: str) -> None:
        job: Job = self.get_job(id)

        if type == "resume":
            shutil.copy(file, Path("./db/resumes/"))
            job.resume = "./db/resumes/" + file.name
        elif type == "coverLetter":
            shutil.copy(file, Path("./db/coverLetters/"))
            job.coverLetter = "./db/coverLetters/" + file.name

        self.update_job(job)

