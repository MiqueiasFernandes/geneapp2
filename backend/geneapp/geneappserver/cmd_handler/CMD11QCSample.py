from .CMD_Handler import CMD_Handler

class CMD11QCSample(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(11)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        sample, param, is_pe = command.arg1, command.arg2, 1 if command.arg3 == "1" else 0
        command.tsp = self.job_post(f"qcsample/{prj}/{id}/{sample}/{is_pe}/{lock}", {"param": param})
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
