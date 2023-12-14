from ..models import Command
import requests
import os
from ..geneappscript import GENEAPPSCRIPT_API, LOCAL, PROJECTS

class CMD_Handler:

    def __init__(self, op) -> None:
        self.op = op
        self.GENEAPPSCRIPT_API = GENEAPPSCRIPT_API

    def handle(self, command):
        if (command.op == self.op):
            return self.run(command)
        return False
    
    def run(self, command: Command) -> int:
        raise NotImplementedError("Implementar handdler")
    
    def job_get(self, url):
        try:
            resp = requests.get(f"{GENEAPPSCRIPT_API}/{url}")
            json = resp.json()
            return json['job']['job'] if json['success'] else 0
        except:
            return 0

    def job_post(self, url, json):
        try:
            resp = requests.post(f"{GENEAPPSCRIPT_API}/{url}", json=json)
            json = resp.json()
            return json['job']['job'] if json['success'] else 0
        except:
            return 0

