from .CMD_Handler import CMD_Handler

class CMD20Deeptools(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(20)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        command.tsp = self.job_get(f"deeptools/{prj}/{id}/{lock}")
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
