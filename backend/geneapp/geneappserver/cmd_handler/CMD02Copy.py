from .CMD_Handler import CMD_Handler

class CMD02Copy(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(2)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        fin, fout = command.arg1, command.arg2
        command.tsp = self.job_get(f"{self.GENEAPPSCRIPT_API}/copiar/{prj}/{id}/{fin}/{fout}")
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False

