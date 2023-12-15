#!/usr/bin/env bash
set -e

source /flask_env/bin/activate

export DATA_DIR=/tmp/geneappdata
export PROJECTS=$DATA_DIR/projects
export LIMIT="${SERVICE_LIMIT:-5}"

export TS_ONFINISH=/app/scripts/_jobend.sh
export TS_SLOTS="${SERVICE_JOBS:-2}"
export TMPDIR=/tmp ####$DATA_DIR/jobs
export TS_SAVELIST=$DATA_DIR/tsp.jobs.txt

export FLASK_APP=geneappscript.py
export FLASK_ENV="${FLASK_PROF:-development}"
export FLASK_RUN_HOST="${FLASK_HOST:-0.0.0.0}"
export FLASK_RUN_PORT="${FLASK_PORT:-9000}"
export FLASK_API="${FLASK_API:-localhost:9000}"

( tsp || ([ ! -d "$TMPDIR" ] && mkdir -p $TMPDIR && tsp) ) > /dev/null

if [ "$1" = 'flask' ]; then
    [ ! -d "$PROJECTS" ] && mkdir -p $PROJECTS
    [ "$FLASK_ENV" = "development" ] && DBG="--debug"
fi

exec "$@" $DBG