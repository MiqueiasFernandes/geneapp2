from .CMD_Handler import CMD_Handler

class CMD04Unzip(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(4)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        path = command.arg1
        command.tsp = self.job_get(f"unzip/{prj}/{id}/{path}/{lock}")
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False

