
import time
import requests
import os

GENEAPPSCRIPT_API = f"http://{os.environ.get('GENEAPPSERVICEA_PI', 'localhost:9000')}"
LOCAL = '/tmp/geneappdata' if os.environ.get('DJANGO_PROF') == 'PRD' else '/Users/miqueias/Local/geneapp2/data'

def criar_proj():
    path = requests.get(GENEAPPSCRIPT_API+'/criar_projeto').text
    time.sleep(3)
    return path

def write_data(fd, dt):
    with open(f"{LOCAL}/{fd}", 'w') as fo:
        fo.write(dt)

