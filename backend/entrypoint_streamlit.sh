#!/bin/bash
source /opt/conda/etc/profile.d/conda.sh
conda activate $(head -1 environment.yml | cut -d' ' -f2)

streamlit run streamlit_dashboard.py \
  --server.port 8501 \
  --server.address 0.0.0.0