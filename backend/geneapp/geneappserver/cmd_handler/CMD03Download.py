from .CMD_Handler import CMD_Handler

class CMD03Download(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(3)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        url, fout = command.arg1, command.arg2
        sra, pe = 1 if command.arg3== 'sra' else 9, 1 if command.project.library == "SHORT_PAIRED" else 9
        command.tsp = self.job_post(f"baixar/{prj}/{id}/{fout}/{sra}/{pe}/{lock}", {"url": url})
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
