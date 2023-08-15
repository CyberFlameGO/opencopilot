#!/bin/bash
source /opt/conda/etc/profile.d/conda.sh
conda activate $(head -1 environment.yml | cut -d' ' -f2)

echo "Ingesting data"
python ingest_data.py

# TODO: for production use we need to increase this number but how?
# cpu_units=$(getconf _NPROCESSORS_ONLN)
workers_to_spawn=1
echo "Starting service with ${workers_to_spawn} workers"
gunicorn --log-level debug --timeout 300 --bind 0.0.0.0:8000 --worker-class=uvicorn.workers.UvicornWorker --workers=$workers_to_spawn app:app
