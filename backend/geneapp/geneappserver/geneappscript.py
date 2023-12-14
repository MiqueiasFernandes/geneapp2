import requests
import os
from datetime import datetime, timezone

GENEAPPSCRIPT_API = f"http://{os.environ.get('GENEAPPSERVICEA_PI', 'localhost:9000')}"
LOCAL = '/tmp/geneappdata' if os.environ.get('DJANGO_PROF') == 'PRD' else '/Users/miqueias/Local/geneapp2/data'
PROJECTS = f"{LOCAL}/projects"

def criar_proj():
    resp = requests.get(GENEAPPSCRIPT_API+'/criar_projeto')
    json = resp.json()
    job = json['job']
    return job['prj']

def rm_proj(path):
    return requests.get(GENEAPPSCRIPT_API+'/remover_projeto/' + path).text == "ok"

def write_data(prj, fd, dt):
    with open(f"{PROJECTS}/{prj}/{fd}", 'w') as fo:
        fo.write(dt)

def get_logs(prj, id):
    log, out, err = '', '', ''
    
    with open(f"{PROJECTS}/{prj}/jobs/job.{id}.log.txt") as fin:
        log = fin.read()[-950:]

    with open(f"{PROJECTS}/{prj}/jobs/job.{id}.out.txt") as fin:
        out = fin.read()[-950:]

    with open(f"{PROJECTS}/{prj}/jobs/job.{id}.err.txt") as fin:
        err = fin.read()[-950:]

    return log, out, err

def get_time(prj, id):
    started, ended = "", ""
    try:
        with open(f"{PROJECTS}/{prj}/jobs/jobs.txt") as fin:
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
    resp = requests.get(f"{GENEAPPSCRIPT_API}/job_status/{id}")
    return resp.json()


# def __job_get(url):
#     try:
#         resp = requests.get(url)
#         json = resp.json()
#         return json['job']['job'] if json['success'] else 0
#     except:
#         return 0

# def __job_post(url, json):
    try:
        resp = requests.post(url, json=json)
        json = resp.json()
        return json['job']['job'] if json['success'] else 0
    except:
        return 0
