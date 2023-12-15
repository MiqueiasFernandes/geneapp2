import requests
from datetime import datetime, timezone
from geneapp.env import ENV_GENEAPP_SERVICE_API, ENV_PROJECTS

def criar_proj():
    resp = requests.get(ENV_GENEAPP_SERVICE_API+'/criar_projeto')
    json = resp.json()
    job = json['job']
    return job['prj']

def rm_proj(path):
    return requests.get(ENV_GENEAPP_SERVICE_API+'/remover_projeto/' + path).text == "ok"

def write_data(prj, fd, dt):
    with open(f"{ENV_PROJECTS}/{prj}/{fd}", 'w') as fo:
        fo.write(dt)

def get_logs(prj, id):
    fnf = 'FILE NOT FOUND'
    log, out, err = f'!!! LOG {fnf} !!!', f'!!! OUT {fnf} !!!', f'!!! ERROR {fnf} !!!'
    
    with open(f"{ENV_PROJECTS}/{prj}/jobs/job.{id}.log.txt") as fin:
        log = fin.read()[-950:]

    with open(f"{ENV_PROJECTS}/{prj}/jobs/job.{id}.out.txt") as fin:
        out = fin.read()[-950:]

    with open(f"{ENV_PROJECTS}/{prj}/jobs/job.{id}.err.txt") as fin:
        err = fin.read()[-950:]

    return log, out, err

def get_time(prj, id):
    started, ended = "", ""
    try:
        with open(f"{ENV_PROJECTS}/{prj}/jobs/jobs.txt") as fin:
            for line in fin:
                if line.startswith(f"S {id} "):
                    started = line.strip().split(" ")[2][:45]
                if line.startswith(f"E {id} "):
                    ended = line.strip().split(" ")[2][:45]
            if len(started) > 10 and len(ended) < 10:
                ended = datetime.now(timezone.utc).replace(microsecond=0).astimezone().isoformat()
    except:
        pass
    return started, ended

##"/job_status/<int:id>"
def job_status(id):
    resp = requests.get(f"{ENV_GENEAPP_SERVICE_API}/job_status/{id}")
    return resp.json()
