import time
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
    time.sleep(2)
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


def __job_get(url):
    try:
        resp = requests.get(url)
        json = resp.json()
        return json['job']['job'] if json['success'] else 0
    except:
        return 0

def __job_post(url, json):
    try:
        resp = requests.post(url, json=json)
        json = resp.json()
        return json['job']['job'] if json['success'] else 0
    except:
        return 0

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
## /unzip/<proj>/<int:id>/<path>/<int:lock>
def job_unzip(prj, id, path, lock=0):
    return __job_get(f"{GENEAPPSCRIPT_API}/unzip/{prj}/{id}/{path}/{lock}")

## OP = 5
## /qinput/<proj>/<int:id>/<fg>/<fa>/<ft>/<fp>/<int:lock>
def job_qinput(prj, id, fg, fa, ft, fp, lock=0):
    return __job_get(f"{GENEAPPSCRIPT_API}/qinput/{prj}/{id}/{fg}/{fa}/{ft}/{fp}/{lock}")

## OP = 6
## /splitx/<proj>/<int:id>/<fg>/<fa>
def job_splitx(prj, id, fg, fa):
    return __job_get(f"{GENEAPPSCRIPT_API}/splitx/{prj}/{id}/{fg}/{fa}")

## OP = 7
## /joinx/<proj>/<int:id>/<fg>/<fa>
def job_joinx(prj, id, fg, fa, lock=0):
    return __job_get(f"{GENEAPPSCRIPT_API}/joinx/{prj}/{id}/{fg}/{fa}/{lock}")

## OP = 8
## /holder/<proj>/<int:id>/<int:p1>/<int:p2>/<int:p3>/<int:p4>/<int:p5>/<int:p6>>
def job_holder(prj, id, p1, p2=0, p3=0, p4=0, p5=0, p6=0):
    return __job_get(f"{GENEAPPSCRIPT_API}/holder/{prj}/{id}/{p1}/{p2}/{p3}/{p4}/{p5}/{p6}")