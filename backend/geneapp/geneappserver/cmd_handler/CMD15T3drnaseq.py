from .CMD_Handler import CMD_Handler

class CMD15T3drnaseq(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(15)
    
    ##<bam1>/<bam2>/<int:rlen>
    def run(self, command):
        prj, id, lock = command.project.path, command.id, command.lock
        ctrl, trt, param = command.arg1, command.arg2, command.payload
        command.tsp = self.job_post(f"t3drnaseq/{prj}/{id}/{ctrl}/{trt}/{lock}", {"samples": param.split("\n")})
        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False
