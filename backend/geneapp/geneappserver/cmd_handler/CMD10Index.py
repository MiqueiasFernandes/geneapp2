from .CMD_Handler import CMD_Handler

class CMD10Index(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(10)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        fg, idx, is_salmon = command.arg1, command.arg2, 1 if command.arg3 == "1" else 0
        command.tsp = self.job_get(f"index/{prj}/{id}/{fg}/{idx}/{is_salmon}/{lock}")
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
