from .CMD_Handler import CMD_Handler

class CMD06Splitx(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(6)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        fg, fa = command.arg1, command.arg2
        command.tsp = self.job_get(f"{self.GENEAPPSCRIPT_API}/splitx/{prj}/{id}/{fg}/{fa}")
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False

