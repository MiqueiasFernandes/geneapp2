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
BASIC_STR = re.compile(r"^[A-Za-z0-9@ ,:/_.-]{4,200}$")
SLOTS=os.environ.get('TS_SLOTS', "1")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100000000

print(f"""
starting GeneAPPSERVICE {LOCAL} => {datetime.today().strftime('%Y-%m-%d %HH%M')} [{LIMIT} / {SLOTS}]....
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
    tsp = "tsp is ok."
    try:
        if not os.path.isdir(INPUTS):
            os.makedirs(INPUTS)
        Popen(["tsp", "-S", SLOTS], stdout=PIPE, stderr=PIPE)
        p = Popen(["tsp", "-S"], stdout=PIPE, stderr=PIPE)
        output, _ = p.communicate()
        slots = int(output.decode('utf-8'))
        if slots > 0:
            tsp = f"tsp has {slots} slots"
        else:
            tsp = "error in tsp."
    except:
        store = 'ERROR in store.'
    return {"store": store, "paths": [PROJECTS, INPUTS], "tsp": tsp, "projects": os.listdir(PROJECTS)}


## ## ## PROJECT CONTROL
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

projects = [x for x in os.listdir(PROJECTS) if x.startswith("geneapp@")]

@app.route("/criar_projeto")
def criar_projeto():
    assert len(os.listdir(PROJECTS)) < LIMIT
    id = str(uuid.uuid4())
    local = datetime.today().strftime("%Y-%m-%d")
    proj = f'geneapp@{local}_{id}'
    os.makedirs(f"{PROJECTS}/{proj}/inputs")
    os.makedirs(f"{PROJECTS}/{proj}/jobs")
    os.makedirs(f"{PROJECTS}/{proj}/results")
    projects.append(proj)
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
        self.args = list(map(str,args))
        self.status = 'created'
        self.job = None ### id do tsp
        self.end = False
        self.success = False

    def lock(self, tsp_id):
        self.args.insert(0, str(tsp_id))
        self.args.insert(0, "-D")

    def run(self):
        """
        Job workflow
            1. registrar job aqui [DJANGO, TSP, PRJ]
            2. enfileirar no tsp
            3. tsp executa o job
            -4. django obtem status via GET
            -4. tsp copia log para o proj via POST job_status
        """
        p = Popen(["tsp"] + self.args, stdout=PIPE, stderr=PIPE)
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

def make_job(proj:str, id:int, args, lock=None):
    job = Job(proj, id, args)
    if not lock is None:
        job.lock(lock)
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
    try:
        external = external.strip().replace('..', '.')
        assert re.fullmatch(BASIC_STR, external) 
        assert (not external.startswith('/')) and (not external.endswith('/'))
        assert allow(external)
    except:
        raise Exception(f"STR INV: {external} FN: {allow}")
    return external

@app.route("/show/<proj>/<int:id>/<file>", methods=['POST'])
def show(proj, id, file): ## salvar texto na pasta results
    assert id >= 0 and proj in projects
    request_data = request.get_json()
    msg = clean(request_data['msg'], allow=lambda e: True)
    return make_job(proj, id, [f"{SCRIPTS}/show.sh", PROJECTS, proj, id, file, msg])

@app.route("/copiar/<proj>/<int:id>/<fin>/<fout>")
def copiar(proj, id, fin, fout): ## copiar do inputs geral para o inputs do projeto
    assert id >= 0 and proj in projects
    src = clean(fin, lambda f: f in os.listdir(f'{INPUTS}'))
    dst = clean(fout, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/copiar.sh", PROJECTS, proj, id, src, dst])

@app.route("/baixar/<proj>/<int:id>/<out>/<int:sra>/<int:paired>", methods=['POST'])
def baixar(proj, id, out, sra, paired): ## baixar no inputs do projeto
    assert id >= 0 and proj in projects
    request_data = request.get_json()
    url = clean(request_data['url'], lambda _: True) if sra == 1 else clean(request_data['url'])
    dst = clean(out, lambda _: True)
    args = [f"{SCRIPTS}/baixar.sh", PROJECTS, proj, id, url, dst]
    if sra == 1:
        args.append("1")
        if paired == 1:
            args.append("1")
    return make_job(proj, id, args)

@app.route("/unzip/<proj>/<int:id>/<path>/<int:lock>")
def unzip(proj, id, path, lock: int): ## abrir aquivo ou pasta da pasta no inputs do projeto
    assert id >= 0 and proj in projects
    src = clean(path, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/zip.sh", PROJECTS, proj, id, src], lock if lock > 0 else None)

@app.route("/zip/<proj>/<int:id>/<path>")
def zip(proj, id, path): ## comprimir aquivo ou pasta da pasta do inputs do projeto
    assert id >= 0 and proj in projects
    src = clean(path, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/zip.sh", PROJECTS, proj, id, src, 1])

@app.route("/qinput/<proj>/<int:id>/<fg>/<fa>/<ft>/<fp>/<int:lock>")
def qinput(proj, id, fg, fa, ft, fp, lock: int): ## validar arquivos de entrada
    assert id >= 0 and proj in projects
    fg = clean(fg, lambda _: True)
    fa = clean(fa, lambda _: True)
    ft = clean(ft, lambda _: True)
    fp = clean(fp, lambda _: True)
    return make_job(proj, id, [f"{SCRIPTS}/qinput.py", PROJECTS, proj, id, fg, fa, ft, fp], lock if lock > 0 else None)

@app.route("/splitx/<proj>/<int:id>/<fg>/<fa>")
def splitx(proj, id, fg, fa): ## dividir arquivos de entrada
    assert id >= 0 and proj in projects
    fg = clean(fg, lambda f: f in os.listdir(f'{INPUTS}'))
    fa = clean(fa, lambda f: f in os.listdir(f'{INPUTS}'))
    return make_job(proj, id, [f"{SCRIPTS}/splitx.py", PROJECTS, proj, id, fg, fa])

@app.route("/joinx/<proj>/<int:id>/<fg>/<fa>/<int:lock>")
def joinx(proj, id, fg, fa, lock: int): ## juntar results arquivos de entrada
    assert id >= 0 and proj in projects
    fg = clean(fg, lambda f: f in os.listdir(f'{INPUTS}'))
    fa = clean(fa, lambda f: f in os.listdir(f'{INPUTS}'))
    return make_job(proj, id, [f"{SCRIPTS}/joinx.sh", PROJECTS, proj, id, fg, fa], lock if lock > 0 else None)

@app.route("/holder/<proj>/<int:id>/<int:p1>/<int:p2>/<int:p3>/<int:p4>/<int:p5>/<int:p6>")
def holder(proj, id, p1, p2, p3, p4, p5, p6): ## segurar ate finalizar jobs dependencia
    assert id >= 0 and proj in projects and p1 > 0
    args = [f"{SCRIPTS}/holder.sh", PROJECTS, proj, id, p1]
    if p2 > 0: args.append(p2)
    if p3 > 0: args.append(p3)
    if p4 > 0: args.append(p4)
    if p5 > 0: args.append(p5)
    if p6 > 0: args.append(p6)
    return make_job(proj, id, args)


server()
