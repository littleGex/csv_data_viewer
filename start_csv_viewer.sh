#!/bin/sh
# conda env list

DIRNAME=$(dirname "$0")

src_path=$DIRNAME/src/csvTableUI.py

# Start conda environment
# conda activate <enter_env_name>

# Run UI
python $src_path "$@"
