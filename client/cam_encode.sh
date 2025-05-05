#!/bin/bash
PROJECT_ROOT=/home/admin/pyUSBcap
LOG=$PROJECT_ROOT/log
TS=$(date "+%Y%m%d%H%M%S")
# shellcheck disable=SC2164
cd $PROJECT_ROOT/client
. ../.venv/bin/activate
python3 encode.py &> $LOG/$TS-encode.log
