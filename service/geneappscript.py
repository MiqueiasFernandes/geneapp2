from flask import Flask, request
import uuid
import os
import sys
import re
import shutil
from datetime import datetime
from subprocess import Popen, PIPE

LOCAL=os.environ.get("DATA_DIR")
PROF=os.environ.get("FLASK_ENV")
LIMIT=int(os.environ.get("LIMIT", "0"))
SLOTS=int(os.environ.get('TS_SLOTS', "0"))

assert LOCAL != "" and LIMIT > 0 and SLOTS > 0

PROJECTS=LOCAL+'/projects'
SCRIPTS='/app/scripts'
INPUTS=PROJECTS+'/inputs'
VOID=('', 204)
ALLOW = ['http://ftp.ncbi.nlm.nih.gov/', 'https://ftp.ncbi.nlm.nih.gov/']
BASIC_STR = re.compile(r"^[A-Za-z0-9@ ,:/_.-]{4,200}$")

app = Flask(__name__)
##app.config["MAX_CONTENT_LENGTH"] = 100000000

print(f"""
         .....  SERVICE [{LIMIT} / {SLOTS}] => {PROF}  ....
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
    tsp = "tsp is NOT ok."
    try:
        if not os.path.isdir(INPUTS):
            os.makedirs(INPUTS)
        Popen(["tsp", "-S", str(SLOTS)], stdout=PIPE, stderr=PIPE)
        p = Popen(["tsp", "-S"], stdout=PIPE, stderr=PIPE)
        output, _ = p.communicate()
        if int(output.decode('utf-8')) == SLOTS:
            tsp = f"tsp has {SLOTS} slots"
        else:
            tsp = "error in tsp."
    except:
        store = 'ERROR in store.'
    return {
        "store": store, 
        "paths": [PROJECTS, INPUTS], 
        "tsp": tsp, 
        "projects": os.listdir(PROJECTS),
        "env":[SLOTS, LIMIT]
    }


## ## ## PROJECT CONTROL
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

projects = [x for x in os.listdir(PROJECTS) if x.startswith("geneapp@")]

@app.route("/criar_projeto")
def criar_projeto():
    assert len([x for x in os.listdir(PROJECTS) if x.startswith("geneapp@")]) < LIMIT
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
        if self.args[0].endswith(".py"):
            self.args.insert(0, "/app/scripts/_py" )
        self.status = 'created'
        self.job = None ### id do tsp
        self.end = False
        self.success = False
        self.logf = f"{PROJECTS}/{self.prj}/jobs/job.{self.id}.log.txt"

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

    def finish(self, ss=False, st=None):
        self.status = 'finished' if st is None else st
        self.end = True
        self.success = ss

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
    job.finish()
    try:
        output_filename = request_data['output_filename']
        shutil.copyfile(output_filename, job.logf)
        job.finish(open(job.logf).read().endswith("TERMINADO_COM_SUCESSO\n"))
    except:
        print(f"JOB FINISH ERROR: {request_data}", file=sys.stderr)
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
    ##running, queued, finished, skipped
    if job.status == 'skipped':
        job.finish(st = 'skipped')
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

def _clean(external, allow):
    try:
        external = external.replace('\\', '/').replace('..', '.')
        external = f"{external.strip()}"
        assert re.fullmatch(BASIC_STR, external) 
        assert (not external.startswith('/')) and (not external.endswith('/'))
        assert allow(external)
    except:
        raise Exception(f"STR INV: {external} FN: {allow}")
    return external

cln_str = lambda e: _clean(e, lambda _: True)
cln_url = lambda e: _clean(e, lambda f: any([f.startswith(x) for x in ALLOW]))
cln_input = lambda e: _clean(e, lambda f: f in os.listdir(INPUTS))

@app.route("/show/<proj>/<int:id>/<file>", methods=['POST'])
def show(proj, id, file): ## salvar texto na pasta results
    assert id >= 0 and proj in projects
    request_data = request.get_json()
    msg = f'msg.{id}.txt'
    open(f'{INPUTS}/{msg}', 'w').write(request_data['msg'])
    return make_job(proj, id, [f"{SCRIPTS}/show.sh", PROJECTS, proj, id, file, msg])

@app.route("/copiar/<proj>/<int:id>/<fin>/<fout>/<int:lock>")
def copiar(proj, id, fin, fout, lock): ## copiar do inputs geral para o inputs do projeto
    assert id >= 0 and proj in projects
    src = cln_input(fin)
    dst = cln_str(fout)
    return make_job(proj, id, [f"{SCRIPTS}/copiar.sh", PROJECTS, proj, id, src, dst], lock)

@app.route("/baixar/<proj>/<int:id>/<out>/<int:sra>/<int:paired>/<int:lock>", methods=['POST'])
def baixar(proj, id, out, sra, paired, lock): ## baixar no inputs do projeto
    assert id >= 0 and proj in projects
    request_data = request.get_json()
    url = cln_url(request_data['url']) if sra == 1 else cln_url(request_data['url'])
    dst = cln_str(out)
    args = [f"{SCRIPTS}/baixar.sh", PROJECTS, proj, id, url, dst]
    if sra == 1:
        args.append("1")
        if paired == 1:
            args.append("1")
    return make_job(proj, id, args, lock)

@app.route("/unzip/<proj>/<int:id>/<path>/<int:lock>")
def unzip(proj, id, path, lock: int): ## abrir aquivo ou pasta da pasta no inputs do projeto
    assert id >= 0 and proj in projects
    src = cln_str(path)
    return make_job(proj, id, [f"{SCRIPTS}/zip.sh", PROJECTS, proj, id, src], lock if lock > 0 else None)

@app.route("/zip/<proj>/<int:id>/<path>")
def zip(proj, id, path): ## comprimir aquivo ou pasta da pasta do inputs do projeto
    assert id >= 0 and proj in projects
    src = cln_str(path)
    return make_job(proj, id, [f"{SCRIPTS}/zip.sh", PROJECTS, proj, id, src, 1])

@app.route("/qinput/<proj>/<int:id>/<fg>/<fa>/<ft>/<fp>/<int:lock>")
def qinput(proj, id, fg, fa, ft, fp, lock: int): ## validar arquivos de entrada
    assert id >= 0 and proj in projects
    fg = cln_str(fg)
    fa = cln_str(fa)
    ft = cln_str(ft)
    fp = cln_str(fp)
    return make_job(proj, id, [f"{SCRIPTS}/qinput.py", PROJECTS, proj, id, fg, fa, ft, fp], lock if lock > 0 else None)

@app.route("/qinput2/<proj>/<int:id>/<fg>/<fa>/<novo_gff>/<fasta_genes>/<int:lock>")
def qinput2(proj, id, fg, fa, novo_gff, fasta_genes, lock: int): ## validar arquivos de entrada
    assert id >= 0 and proj in projects
    fg = cln_str(fg)
    fa = cln_str(fa)
    ft = cln_str(novo_gff)
    fp = cln_str(fasta_genes)
    return make_job(proj, id, [f"{SCRIPTS}/qinput.sh", PROJECTS, proj, id, fg, fa, ft, fp], lock if lock > 0 else None)

@app.route("/splitx/<proj>/<int:id>/<fg>/<fa>")
def splitx(proj, id, fg, fa): ## dividir arquivos de entrada
    assert id >= 0 and proj in projects
    fg = cln_str(fg)
    fa = cln_str(fa)
    return make_job(proj, id, [f"{SCRIPTS}/splitx.py", PROJECTS, proj, id, fg, fa])

@app.route("/joinx/<proj>/<int:id>/<fg>/<fa>/<int:lock>")
def joinx(proj, id, fg, fa, lock: int): ## juntar results arquivos de entrada
    assert id >= 0 and proj in projects
    fg = cln_str(fg)
    fa = cln_str(fa)
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

@app.route("/index/<proj>/<int:id>/<fg>/<idx>/<int:is_salmon>/<int:lock>")
def index(proj, id, fg, idx, is_salmon, lock: int): ## index genomic files
    assert id >= 0 and proj in projects
    fg = cln_str(fg)
    idx = cln_str(idx)
    args = [f"{SCRIPTS}/indexar.sh", PROJECTS, proj, id, fg, idx]
    if is_salmon == 1:
        args.append(1)
    return make_job(proj, id, args, lock if lock > 0 else None)

@app.route("/qcsample/<proj>/<int:id>/<sample>/<int:is_pe>/<int:lock>", methods=['POST'])
def qcsample(proj, id, sample, is_pe, lock: int): ## quality control for fastq short reads
    assert id >= 0 and proj in projects
    sample = cln_str(sample)
    request_data = request.get_json()
    param =  cln_str(request_data['param'])
    args = [f"{SCRIPTS}/qcsample.sh", PROJECTS, proj, id, sample, param]
    if is_pe == 1:
        args.append(1)
    return make_job(proj, id, args, lock if lock > 0 else None)

@app.route("/mapping/<proj>/<int:id>/<sample>/<index>/<int:is_pe>/<int:lock>", methods=['POST'])
def mapping(proj, id, sample, index, is_pe, lock: int): ## maping in indexed genomic files
    assert id >= 0 and proj in projects
    sample = cln_str(sample)
    index = cln_str(index)
    request_data = request.get_json()
    param =  cln_str(request_data['param'])
    args = [f"{SCRIPTS}/mapping.sh", PROJECTS, proj, id, sample, index, param]
    if is_pe == 1:
        args.append(1)
    return make_job(proj, id, args, lock if lock > 0 else None)

@app.route("/quantify/<proj>/<int:id>/<sample>/<index>/<int:is_pe>/<int:lock>", methods=['POST'])
def quantify(proj, id, sample, index, is_pe, lock: int): ## quantify in indexed genomic files
    assert id >= 0 and proj in projects
    sample = cln_str(sample)
    index = cln_str(index)
    request_data = request.get_json()
    param =  cln_str(request_data['param'])
    args = [f"{SCRIPTS}/quantify.sh", PROJECTS, proj, id, sample, index, param]
    if is_pe == 1:
        args.append(1)
    return make_job(proj, id, args, lock if lock > 0 else None)

server()
