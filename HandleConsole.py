import inquirer
import datetime
import re
from enum import Enum
from Job import Job

# rich
from rich.console import Console
from rich.table import Table
from rich.rule import Rule
from rich.tree import Tree
import rich.box

class ConsoleCommands(Enum):
    LIST = 1
    LIST_ID = 2
    ADD = 3
    EDIT = 4
    DELETE = 5
    QUIT = 6


class HandleConsole:
    def __init__(self):
        self._rich_console: Console = Console()

    # helper methods

    def _validate_date(self, date: str) -> bool:
        if date == "":
            return True
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            return True
        
        raise inquirer.errors.ValidationError(
            "", reason="Please enter a valid date in the format YYYY-MM-DD"
        )
    
    def _parse_date(self, date: str) -> str:
        if date == "":
            return datetime.date.today().strftime("%Y-%m-%d")
        
        return date
    
    def _stylize_status(self, status: str) -> str:
        if status == "applied":
            return f"[green]{status.capitalize()}[/green]"
        elif status == "interview" or status == "technical":
            return f"[yellow]{status.capitalize()}[/yellow]"
        elif status == "offer":
            return f"[blue]{status.capitalize()}[/blue]"
        elif status == "rejected" or status == "ghosted" or status == "withdrawn":
            return f"[red]{status.capitalize()}[/red]"

    # public methods

    def error(self, error: str) -> None:
        self._rich_console.print(f"[bold red]Error:[/bold red] {error}\n")

    def get_command(self) -> ConsoleCommands:
        questions = [
            inquirer.List(
                "command",
                message="What would you like to do?",
                choices=[
                    ("List all jobs", ConsoleCommands.LIST),
                    ("List job by id", ConsoleCommands.LIST_ID),
                    ("Add a job", ConsoleCommands.ADD),
                    ("Edit a job", ConsoleCommands.EDIT),
                    ("Delete a job", ConsoleCommands.DELETE),
                    ("Quit", ConsoleCommands.QUIT),
                ],
            )
        ]

        return inquirer.prompt(questions)["command"]
    
    def get_job_id(self) -> int:
        questions = [
            inquirer.Text(
                "job_id",
                message="Enter the job id",
            )
        ]

        return int(inquirer.prompt(questions)["job_id"])

    def list_jobs(self, jobs: list[Job]) -> None:
        jobTable: Table = Table(title="Job List", box=rich.box.SIMPLE)

        jobTable.add_column("ID", justify="center", style="cyan")
        jobTable.add_column("Date Applied", justify="center", style="cyan")
        jobTable.add_column("Company", justify="left")
        jobTable.add_column("Position", justify="left")
        jobTable.add_column("Job Board", justify="left")
        jobTable.add_column("Website", justify="left")
        jobTable.add_column("Resume", justify="left")
        jobTable.add_column("Cover Letter", justify="left")
        jobTable.add_column("Latest Status", justify="right")

        for job in jobs:
            stringList = [
                str(job.id),
                str(job.dateApplied),
                job.company,
                job.position,
                f"[link={job.jobBoard}]{job.jobBoard}[/link]",
                f"[link={job.website}]{job.website}[/link]",
                job.resume,
                job.coverLetter,
                self._stylize_status(job.statusList[-1]),
            ]

            jobTable.add_row(*stringList)

        self._rich_console.print(jobTable)
        self._rich_console.print('\n')

    def list_job(self, job: Job) -> None:
        self._rich_console.print(Rule(
            title=f"[bold]Job Details for [cyan]ID {job.id}[/cyan][/bold]",
            align="center"
        ))

        self._rich_console.print(f"[bold cyan]Date Applied:[/bold cyan] {job.dateApplied}")
        self._rich_console.print(f"[bold cyan]Company:[/bold cyan] {job.company}")
        self._rich_console.print(f"[bold cyan]Position:[/bold cyan] {job.position}")
        self._rich_console.print(f"[bold cyan]Job Board:[/bold cyan] [link={job.jobBoard}]{job.jobBoard}[/link]")
        self._rich_console.print(f"[bold cyan]Website:[/bold cyan] [link={job.website}]{job.website}[/link]")
        self._rich_console.print(f"[bold cyan]Resume:[/bold cyan] {job.resume}")
        self._rich_console.print(f"[bold cyan]Cover Letter:[/bold cyan] {job.coverLetter}")
        self._rich_console.print(f"[bold cyan]Status Tree:[/bold cyan]")

        statusTree: Tree = Tree(self._stylize_status(job.statusList[0]))

        returner: Tree = statusTree
        for status in job.statusList[1:]:
            returner = returner.add(self._stylize_status(status))

        self._rich_console.print(statusTree)
        self._rich_console.print('\n')
    
    def add_job(self) -> Job:
        questions = [
            inquirer.Text(
                "date_applied",
                message="Enter the date applied (YYYY-MM-DD), leave blank for today's date",
                validate=lambda _, x: self._validate_date(x),
            ),
            inquirer.Text(
                "company",
                message="Enter the company name",
            ),
            inquirer.Text(
                "position",
                message="Enter the position name",
            ),
            inquirer.Text(
                "job_board",
                message="Enter the link to the job posting",
            ),
            inquirer.Text(
                "website",
                message="Enter the website you applied on",
            ),
            inquirer.Path(
                "resume",
                message="Enter the path to your resume",
                path_type=inquirer.Path.FILE,
            ),
            inquirer.Path(
                "cover_letter",
                message="Enter the path to your cover letter",
                path_type=inquirer.Path.FILE,
            )
        ]

        answers = inquirer.prompt(questions)

        return Job(
            id=0,
            dateApplied=self._parse_date(answers["date_applied"]),
            company=answers["company"],
            position=answers["position"],
            jobBoard=answers["job_board"],
            website=answers["website"],
            resume=answers["resume"],
            coverLetter=answers["cover_letter"],
            statusList="applied",
        )
    
    def edit_job(self, job: Job) -> Job:
        # ask for each field
        questions = [
            inquirer.Text(
                "date_applied",
                message="Enter the date applied (YYYY-MM-DD), leave blank for today's date",
                default=job.dateApplied,
                validate=lambda _, x: self._validate_date(x),
            ),
            inquirer.Text(
                "company",
                message="Enter the company name",
                default=job.company,
            ),
            inquirer.Text(
                "position",
                message="Enter the position name",
                default=job.position,
            ),
            inquirer.Text(
                "job_board",
                message="Enter the link to the job posting",
                default=job.jobBoard,
            ),
            inquirer.Text(
                "website",
                message="Enter the website you applied on",
                default=job.website,
            ),
            inquirer.Path(
                "resume",
                message="Enter the path to your resume",
                path_type=inquirer.Path.FILE,
                default=job.resume,
            ),
            inquirer.Path(
                "cover_letter",
                message="Enter the path to your cover letter",
                path_type=inquirer.Path.FILE,
                default=job.coverLetter,
            ),
            inquirer.List(
                "status",
                message="Enter most recent status",
                choices=[
                    ("Applied", "applied"),
                    ("Interview", "interview"),
                    ("Technical", "technical"),
                    ("Offer", "offer"),
                    ("Rejected", "rejected"),
                    ("Ghosted", "ghosted"),
                    ("Withdrawn", "withdrawn"),
                    ("No change", "none")
                ],
                default=job.statusList[-1],
            )
        ]

        answers = inquirer.prompt(questions)

        statusList = ">".join(job.statusList)

        if answers["status"] != "none":
            statusList += ">" + answers["status"]

        return Job(
            id=job.id,
            dateApplied=self._parse_date(answers["date_applied"]),
            company=answers["company"],
            position=answers["position"],
            jobBoard=answers["job_board"],
            website=answers["website"],
            resume=answers["resume"],
            coverLetter=answers["cover_letter"],
            statusList=statusList,
        )
    
    def delete_job(self) -> bool:
        questions = [
            inquirer.Confirm(
                "confirm_delete",
                message="Are you sure you want to delete this job?",
                default=False,
            )
        ]

        return inquirer.prompt(questions)["confirm_delete"]
    
    def quit(self) -> None:
        self._rich_console.print("Goodbye!")
