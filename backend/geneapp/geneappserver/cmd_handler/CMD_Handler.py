from ..models import Command
import requests
from geneapp.env import ENV_GENEAPP_SERVICE_API

class CMD_Handler:

    def __init__(self, op) -> None:
        self.op = op

    def handle(self, command):
        if (command.op == self.op):
            return self.run(command)
        return False
    
    def run(self, command: Command) -> int:
        raise NotImplementedError("Implementar handdler")
    
    def job_get(self, url):
        try:
            resp = requests.get(f"{ENV_GENEAPP_SERVICE_API}/{url}")
            json = resp.json()
            return json['job']['job'] if json['success'] else 0
        except:
            return 0

    def job_post(self, url, json):
        try:
            resp = requests.post(f"{ENV_GENEAPP_SERVICE_API}/{url}", json=json)
            json = resp.json()
            return json['job']['job'] if json['success'] else 0
        except:
            return 0

