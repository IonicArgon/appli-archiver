from HandleConsole import HandleConsole
from HandleConsole import ConsoleCommands
from HandleDB import HandleDB

# rich

if __name__ == "__main__":
    handleDB = HandleDB()
    handleConsole = HandleConsole()

    while True:
        command = handleConsole.get_command()

        if command == ConsoleCommands.QUIT:
            handleConsole.quit()
            break

        elif command == ConsoleCommands.LIST:
            jobs = handleDB.get_jobs()
            handleConsole.list_jobs(jobs)

        elif command == ConsoleCommands.LIST_ID:
            id = handleConsole.get_job_id()
            job = None
            try:
                job = handleDB.get_job(id)
            except:
                handleConsole.error("Job not found")

            handleConsole.list_job(job)

        elif command == ConsoleCommands.ADD:
            job = handleConsole.add_job()
            handleDB.add_job(job)

        elif command == ConsoleCommands.EDIT:
            id = handleConsole.get_job_id()
            job = None
            try:
                job = handleDB.get_job(id)
            except:
                handleConsole.error("Job not found")
            
            job = handleConsole.edit_job(job)
            handleDB.update_job(job)

        elif command == ConsoleCommands.DELETE:
            id = handleConsole.get_job_id()
            job = None
            try:
                job = handleDB.get_job(id)
            except:
                handleConsole.error("Job not found")

            if handleConsole.delete_job():
                handleDB.delete_job(id)

        else:
            handleConsole.error("Unknown command")
