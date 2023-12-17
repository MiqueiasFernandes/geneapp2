from .CMD_Handler import CMD_Handler

class CMD13Quantify(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(13)
    
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        sample, index, param, is_pe = command.arg1, command.arg2, command.arg3, 1 if command.arg4 == "1" else 0
        command.tsp = self.job_post(f"quantify/{prj}/{id}/{sample}/{index}/{is_pe}/{lock}", {"param": param})
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
