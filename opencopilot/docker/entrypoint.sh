#!/bin/bash

source /opt/conda/etc/profile.d/conda.sh
conda activate $(head -1 environment.yml | cut -d' ' -f2)

if [ "$#" -eq 0 ]; then
  exec /bin/bash
fi
exec "$@"