from .CMD_Handler import CMD_Handler

class CMD08Holder(CMD_Handler):

    def __init__(self) -> None:
        super().__init__(8)
    
    def run(self, command):

        to_int = lambda x: 0 if x is None else int(x)
        prj, id, lock = command.project.path, command.id, command.lock
        p1, p2, p3 = to_int(command.arg1), to_int(command.arg2), to_int(command.arg3)
        p4, p5, p6 = to_int(command.arg4), to_int(command.arg5), to_int(command.arg6)
        p7, p8, p9 = to_int(command.arg7), to_int(command.arg8), to_int(command.arg9)
        
        command.tsp = self.job_get(f"holder/{prj}/{id}/{p1}/{p2}/{p3}/{p4}/{p5}/{p6}/{p7}/{p8}/{p9}")

        if command.tsp > 0:
            command.status = 'submetido'
            return True
        return False

