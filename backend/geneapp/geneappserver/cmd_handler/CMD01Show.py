from .CMD_Handler import CMD_Handler

class CMD01Show(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(1)
        
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        file, msg = command.arg1, command.arg2
        
        command.tsp = self.job_post(f"show/{prj}/{id}/{file}", {"msg": msg})

        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
