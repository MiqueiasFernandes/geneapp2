from .CMD_Handler import CMD_Handler

class CMD05Qinput(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(5)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        fg, fa, ft, fp = command.arg1, command.arg2, command.arg3, command.arg4
        command.tsp = self.job_get(f"{self.GENEAPPSCRIPT_API}/qinput/{prj}/{id}/{fg}/{fa}/{ft}/{fp}/{lock}")
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
