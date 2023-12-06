from flask import Flask, request
import uuid
import os
import re
import subprocess
from datetime import datetime
from subprocess import Popen, PIPE

LOCAL="/tmp/geneappdata"
PRJ='/projects'
PROJECTS=LOCAL+PRJ
LIMIT=10

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

@app.route("/")
def root():
    return {'geneappservice': 'is running'}

@app.route("/status")
def server():
    store = 'store is ok.'
    try:
        if not os.path.isdir(PROJECTS):
            os.makedirs(f'{PROJECTS}/inputs')
        with open(f'{LOCAL}/server.txt', 'w') as fo:
            fo.write('server ok.\n')
    except:
        store = 'ERROR in store.'
    return {
        "servidor": str(subprocess.run(["ls", "-l", LOCAL], capture_output=True)),
        "store": store
        }

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
    path = f'{PRJ}/{local}_{id}'
    os.makedirs(f"{LOCAL}/{path}/inputs")
    return path



## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

EXP = re.compile(r"^[A-Za-z0-9:/_.-]{4,200}$")

def clean(external):
    external = external.strip().replace('..', '.')
    assert re.fullmatch(EXP, external) 
    assert (not external.startswith('/')) and (not external.endswith('/'))
    return external

@app.route("/copiar_arquivo/<arquivo>/<out>", methods=['POST'])
def copiar_arquivo(arquivo, out):
    ## arquivos sempre sao copiados do /projetos/inputs
    projeto = request.form['projeto']
    p = Popen(["cp", f'{PROJECTS}/inputs/{arquivo}', 
               f'{LOCAL}/{projeto}/inputs/{out}'], 
               stdout=PIPE, stderr=PIPE, user='geneappusr')
    output, error = p.communicate()
    return {'arquivo': out, 
            'status': p.returncode == 0, 
            'log': output.decode('utf-8'), 
            'error': error.decode('utf-8')}

@app.route("/baixar_arquivo/<out>", methods=['POST'])
def baixar_arquivo(out):
    projeto = request.form['projeto']
    arquivo = clean(request.form['arquivo'])
    fo = f'{LOCAL}/{projeto}/inputs/{out}'
    p = Popen(["wget", "-qO", f"{fo}.gz", arquivo], 
              stdout=PIPE, stderr=PIPE, user='geneappusr')
    output, error = p.communicate()
    return {'arquivo': f"{out}.gz", 
            'status': p.returncode == 0, 
            'log': output.decode('utf-8'), 
            'error': error.decode('utf-8')}

@app.route("/descomprimir_arquivo/<arquivo>", methods=['POST'])
def descomprimir_arquivo(arquivo): ## =======>       arquivo.gz
    projeto = request.form['projeto']
    p = Popen(["gunzip", f'{LOCAL}/{projeto}/inputs/{arquivo}'])
    return {'status': p.returncode == 0} ### false





