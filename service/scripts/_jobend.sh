#!/bin/sh

HANDLE=
[ "$#" -eq 0 ] && HANDLE=1 && tsp
[ "$#" -eq 1 ] && HANDLE=1 && tsp -s $1

## programa chamdo pelo TSP quando o job finalizar
## tsp sleep 5 > jobid

[ "$#" -eq 4 ] && HANDLE=1 && \
  curl \
    --header "Content-Type: application/json" \
    --data "{\"jobid\":$1,\"output_filename\":\"$3\"}" \
    -X POST $FLASK_API/job_status
  
# -E Keep stderr apart, in a name like the output file, but adding '.e'.
# -L <lab> name this task with a label, to be distinguished on listing.
# -N <nu m> number of slots required by the job (1 default).

[ $HANDLE ] && exit || echo Usage: ./geneappservice.sh OR ./geneappservice.sh job_id