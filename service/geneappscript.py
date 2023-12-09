from flask import Flask, request
import uuid
import os
import re
import shutil
from datetime import datetime
from subprocess import Popen, PIPE

LOCAL="/tmp/geneappdata"
PROJECTS=LOCAL+'/projects'
SCRIPTS='/app/scripts'
INPUTS=PROJECTS+'/inputs'
VOID=('', 204)
LIMIT=10
ALLOW = ['http://ftp.ncbi.nlm.nih.gov/', 'https://ftp.ncbi.nlm.nih.gov/']
BASIC_STR = re.compile(r"^[A-Za-z0-9:/_.-]{4,200}$")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100000000

print(f"""
starting GeneAPPSERVICE {LOCAL} => {datetime.today().strftime('%Y-%m-%d %HH%M')} [{LIMIT}]....
      ██████╗ ███████╗███╗   ██╗███████╗ █████╗ ██████╗ ██████╗ 
     ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗
     ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████║██████╔╝██████╔╝
     ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██║██╔═══╝ ██╔═══╝ 
     ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║     ██║     
      ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     
                   version 2.0 2023 mikeias.net
""")


## ## ## SERVER CONTROL
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

@app.route("/")
def root():
    return {'geneappservice': 'is running'}

@app.route("/status")
def server():
    store = 'store is ok.'
    try:
        if not os.path.isdir(INPUTS):
            os.makedirs(INPUTS)
    except:
        store = 'ERROR in store.'
    return {"store": store, "paths": [PROJECTS, INPUTS], "projects": os.listdir(PROJECTS)}


## ## ## PROJECT CONTROL
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

@app.route("/criar_projeto")
def criar_projeto():
    assert len(os.listdir(PROJECTS)) < LIMIT
    id = str(uuid.uuid4())
    local = datetime.today().strftime("%Y-%m-%d")
    proj = f'{local}_{id}'
    os.makedirs(f"{PROJECTS}/{proj}/inputs")
    os.makedirs(f"{PROJECTS}/{proj}/jobs")
    os.makedirs(f"{PROJECTS}/{proj}/results")
    return make_job(proj, 0, ["echo", proj])

@app.route("/remover_projeto/<prj>")
def remove_projeto(prj):
    assert prj in os.listdir(PROJECTS)
    shutil.rmtree(f"{PROJECTS}/{prj}")
    return "ok"


## ## ## JOB CONTROL
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

ids = {}
jobs = {}

class Job:
    def __init__(self, prj, id, args=["echo", "OK"]):
        self.prj = prj
        self.id = int(id)  ### id do django
        self.args = ["tsp"] + list(map(str,args))
        self.status = 'created'
        self.job = None ### id do tsp
        self.end = False
        self.success = False

    def run(self):
        """
        Job workflow
            1. registrar job aqui [DJANGO, TSP, PRJ]
            2. enfileirar no tsp
            3. tsp executa o job
            -4. django obtem status via GET
            -4. tsp copia log para o proj via POST job_status
        """
        p = Popen(self.args, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        self.job = int(output.decode('utf-8'))
        return self, p.returncode == 0, error.decode('utf-8')

    def parse(self):
        return {
            "prj": self.prj, 
            "id": self.id, 
            "status": self.status, 
            "job": self.job,
            "args": str(self.args),
            "end": self.end,
            "success": self.success
        }


@app.route("/jobs")
def list_jobs():
    """""
    Essa funcao lista os jobs executados no servidor
    """""
    p = Popen(["tsp"], stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    return '<pre>'+output.decode('utf-8') + error.decode('utf-8')+'</pre>'

@app.route("/job_status", methods=['POST'])
def set_job_status():
    """""
    Essa funcao será chamada automaticamente pelo TSP ao finalizar a execucao de cada job
    """""
    request_data = request.get_json()
    job: Job = jobs[request_data['jobid']]
    output_filename = request_data['output_filename']
    logf = f"{PROJECTS}/{job.prj}/jobs/job.{job.id}.log.txt"
    shutil.copyfile(output_filename, logf)
    job.status = 'finished'
    job.end = True
    job.success = open(logf).read().endswith("TERMINADO_COM_SUCESSO\n")
    return VOID

@app.route("/job_status/<int:id>")
def get_job_status(id: int):
    """""
    Essa rota será usada pelo django para consultar o status do job
    """""
    job: Job = ids[id]
    p = Popen(["tsp", "-s", str(job.job)], stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    job.status = (output.decode('utf-8') + error.decode('utf-8')).strip()
    return job.parse()

def make_job(proj:str, id:int, args):
    job = Job(proj, id, args)
    ids[id] = job
    _, success, err = job.run()
    jobs[job.job] = job
    return {'success': success, 'err': err, 'job': job.parse()}

## ## ## COMMANDS
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

def clean(external, allow=lambda f: any([f.startswith(x) for x in ALLOW])):
    external = external.strip().replace('..', '.')
    assert re.fullmatch(BASIC_STR, external) 
    assert (not external.startswith('/')) and (not external.endswith('/'))
    assert allow(external)
    return external

@app.route("/show/<proj>/<int:id>/<file>", methods=['POST'])
def show(proj, id, file): ## salvar texto na pasta results
    request_data = request.get_json()
    msg = clean(request_data['msg'], allow=lambda e: True)
    return make_job(proj, id, [f"{SCRIPTS}/show.sh", PROJECTS, proj, id, file, msg])

@app.route("/copiar/<proj>/<int:id>/<fin>/<fout>")
def copiar(proj, id, fin, fout): ## copiar do inputs geral para o inputs do projeto
    src = clean(fin, lambda f: f in os.listdir(f'{INPUTS}'))
    dst = clean(fout, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/copiar.sh", PROJECTS, proj, id, src, dst])

@app.route("/baixar/<proj>/<int:id>/<out>", methods=['POST'])
def baixar(proj, id, out): ## baixar no inputs do projeto
    request_data = request.get_json()
    url = clean(request_data['url'])
    dst = clean(out, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/baixar.sh", PROJECTS, proj, id, url, dst])

@app.route("/unzip/<proj>/<int:id>/<path>")
def unzip(proj, id, path): ## abrir aquivo ou pasta da pasta no inputs do projeto
    src = clean(path, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/zip.sh", PROJECTS, proj, id, src])

@app.route("/zip/<proj>/<int:id>/<path>/<fout>")
def zip(proj, id, path, fout): ## comprimir aquivo ou pasta da pasta do inputs do projeto
    src = clean(path, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/zip.sh", PROJECTS, proj, id, src, 1])





server()
