from ..models import Command
import requests
import os

class CMD_Handler:

    def __init__(self, op) -> None:
        self.op = op
        self.GENEAPPSCRIPT_API = f"http://{os.environ.get('GENEAPPSERVICEA_PI', 'localhost:9000')}"
        self.LOCAL = '/tmp/geneappdata' if os.environ.get('DJANGO_PROF') == 'PRD' else '/Users/miqueias/Local/geneapp2/data'
        self.PROJECTS = f"{self.LOCAL}/projects"

    def handle(self, command):
        if (command.op == self.op):
            return self.run(command)
        return False
    
    def run(self, command: Command) -> int:
        raise NotImplementedError("Implementar handdler")
    
    def job_get(self, url):
        try:
            resp = requests.get(url)
            json = resp.json()
            return json['job']['job'] if json['success'] else 0
        except:
            return 0

    def job_post(self, url, json):
        try:
            resp = requests.post(url, json=json)
            json = resp.json()
            return json['job']['job'] if json['success'] else 0
        except:
            return 0

