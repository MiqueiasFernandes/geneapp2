import time
import requests
import os

GENEAPPSCRIPT_API = f"http://{os.environ.get('GENEAPPSERVICEA_PI', 'localhost:9000')}"
LOCAL = '/tmp/geneappdata' if os.environ.get('DJANGO_PROF') == 'PRD' else '/Users/miqueias/Local/geneapp2/data'
PROJECTS = f"{LOCAL}/projects"

def criar_proj():
    resp = requests.get(GENEAPPSCRIPT_API+'/criar_projeto')
    json = resp.json()
    job = json['job']
    time.sleep(3)
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


def __job_get(url):
    try:
        resp = requests.get(url)
        return resp.json()['success']
    except:
        return False

def __job_post(url, json):
    try:
        resp = requests.post(url, json=json)
        return resp.json()['success']
    except:
        return False

##"/job_status/<int:id>"
def job_status(id):
    resp = requests.get(f"{GENEAPPSCRIPT_API}/job_status/{id}")
    return resp.json()

## OP = 1
## /show/<proj>/<int:id>/<file> & POST msg
def job_show(prj, id, file, msg):
    return __job_post(f"{GENEAPPSCRIPT_API}/show/{prj}/{id}/{file}", {"msg": msg})

## OP = 2
## /copiar/<proj>/<int:id>/<fin>/<fout>
def job_copiar(prj, id, fin, fout):
    return __job_get(f"{GENEAPPSCRIPT_API}/copiar/{prj}/{id}/{fin}/{fout}")

## OP = 3
## /baixar/<proj>/<int:id>/<out> & POST url
def job_baixar(prj, id, url, fout, sra, pe):
    return __job_post(f"{GENEAPPSCRIPT_API}/baixar/{prj}/{id}/{fout}/{1 if sra == 'sra' else 9}/{1 if pe else 9}", 
                      {"url": url})

## OP = 4
## /unzip/<proj>/<int:id>/<path>
def job_unzip(prj, id, path):
    return __job_get(f"{GENEAPPSCRIPT_API}/unzip/{prj}/{id}/{path}")

## OP = 5
## /qinput/<proj>/<int:id>/<fg>/<fa>/<ft>/<fp>
def job_qinput(prj, id, fg, fa, ft, fp):
    return __job_get(f"{GENEAPPSCRIPT_API}/qinput/{prj}/{id}/{fg}/{fa}/{ft}/{fp}")

