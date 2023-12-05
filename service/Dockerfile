FROM debian:bookworm

WORKDIR /app
COPY requirements.txt /app
RUN apt update -y && apt install -y python3-pip python3-venv
RUN python3 -m venv /app/flask_env
RUN . /app/flask_env/bin/activate && pip install -r requirements.txt --no-cache-dir
ENV PATH="/app/flask_env/bin:$PATH"

COPY geneappscript.py .

ENV FLASK_APP geneappscript.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]
