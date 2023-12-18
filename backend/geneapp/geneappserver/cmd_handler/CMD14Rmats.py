from .CMD_Handler import CMD_Handler

class CMD14Rmats(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(14)
    
    ##<bam1>/<bam2>/<int:rlen>
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        bam1, bam2, rlen, param = command.arg1, command.arg2, command.arg3, command.arg4
        command.tsp = self.job_post(f"rmats/{prj}/{id}/{bam1}/{bam2}/{rlen}/{lock}", {"param": param})
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
