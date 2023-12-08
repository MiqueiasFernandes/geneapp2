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
        if not os.path.isdir(PROJECTS):
            os.makedirs(INPUTS)
    except:
        store = 'ERROR in store.'
    return store


## ## ## PROJECT CONTROL
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

@app.route("/criar_projeto")
def criar_projeto():
    server()
    assert len(os.listdir(PROJECTS)) < LIMIT
    id = str(uuid.uuid4())
    local = datetime.today().strftime("%Y-%m-%d")
    proj = f'{local}_{id}'
    os.makedirs(f"{PROJECTS}/{proj}/inputs")
    os.makedirs(f"{PROJECTS}/{proj}/jobs")
    os.makedirs(f"{PROJECTS}/{proj}/results")
    return make_job(proj, 0, ["echo", proj])


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
            "args": str(self.args)
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
    shutil.copyfile(output_filename, f"{PROJECTS}/{job.prj}/jobs/job.{job.id}.log.txt")
    job.status = 'finished'
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

@app.route("/copiar/<proj>/<file>/<out>/<int:id>")
def copiar(proj, file, out, id):
    src = clean(file, lambda f: f in os.listdir(f'{INPUTS}'))
    dst = f"{PROJECTS}/{proj}/inputs/{out}"
    return make_job(proj, id, [f"{SCRIPTS}/copiar.sh", PROJECTS, id, proj, f"{INPUTS}/{src}", dst])

@app.route("/baixar/<proj>/<out>/<int:id>", methods=['POST'])
def baixar(proj, out, id):
    request_data = request.get_json()
    url = clean(request_data['url'])
    dst = f"{PROJECTS}/{proj}/inputs/{out}"
    return make_job(proj, id, [f"{SCRIPTS}/baixar.sh", PROJECTS, id, proj, url, dst])

# @app.route("/baixar_arquivo/<out>", methods=['POST'])
# def baixar_arquivo(out):
#     projeto = request.form['projeto']
#     arquivo = clean(request.form['arquivo'])
#     fo = f'{LOCAL}/{projeto}/inputs/{out}'
#     p = Popen(["wget", "-qO", f"{fo}.gz", arquivo], 
#               stdout=PIPE, stderr=PIPE, user='geneappusr')
#     output, error = p.communicate()
#     return {'arquivo': f"{out}.gz", 
#             'status': p.returncode == 0, 
#             'log': output.decode('utf-8'), 
#             'error': error.decode('utf-8')}

# @app.route("/descomprimir_arquivo/<arquivo>", methods=['POST'])
# def descomprimir_arquivo(arquivo): ## =======>       arquivo.gz
#     projeto = request.form['projeto']
#     p = Popen(["gunzip", f'{LOCAL}/{projeto}/inputs/{arquivo}'])
#     return {'status': p.returncode == 0} ### false




server()
