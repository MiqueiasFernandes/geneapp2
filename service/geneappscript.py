from flask import Flask
import uuid
import os
import shutil
from datetime import datetime
import subprocess

LOCAL='/etc/data/projects'
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
        if not os.path.isdir(LOCAL):
            os.mkdir(LOCAL)
        with open(f'{LOCAL}/server.txt', 'w') as fo:
            fo.write('server ok.\n')
    except:
        store = 'ERROR in store.'
    return {
        "servidor": str(subprocess.run(["ls", "-l", "/etc/data"], capture_output=True)),
        "store": store
        }


@app.route("/criar_projeto")
def criar_projeto():
    server()
    assert len(os.listdir(LOCAL)) < LIMIT
    id = str(uuid.uuid4())
    local = datetime.today().strftime("%Y-%m-%d")
    path = f'{LOCAL}/{local}_{id}'
    os.makedirs(path)
    return path
