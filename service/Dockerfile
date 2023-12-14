FROM debian:bookworm

WORKDIR /app
COPY requirements.txt req_env_geneapp.txt geneappservice.sh geneappscript.py /app/

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y task-spooler wget curl zip unzip 
RUN apt install -y sra-toolkit gffread
RUN apt install -y python3-pip python3-venv

RUN python3 -m venv /app/geneapp_env
RUN . /app/geneapp_env/bin/activate && pip install -r req_env_geneapp.txt --no-cache-dir

RUN python3 -m venv /app/flask_env
RUN . /app/flask_env/bin/activate && pip install -r requirements.txt --no-cache-dir
ENV PATH="/app/flask_env/bin:$PATH"

COPY scripts /app/scripts
RUN chmod +x /app/geneappservice.sh /app/scripts/*.sh /app/scripts/*py
ENV TS_ONFINISH=/app/geneappservice.sh
ENV TS_SLOTS=5
#ENV TMPDIR=/tmp/geneappdata/jobs

ENV FLASK_APP geneappscript.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0

#RUN <<EOF
#addgroup -S geneapp
#adduser -S --shell /bin/bash --ingroup geneapp geneappusr
#EOF

CMD ["flask", "run"]
