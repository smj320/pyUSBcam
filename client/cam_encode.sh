#!/bin/bash
PROJECT_ROOT=/home/admin/pyUSBcap
TS=$(date "+%Y%m%d%H%M%S")
LOG=${PROJECT_ROOT}/log/${TS}-encode.log
# shellcheck disable=SC2164
cd $PROJECT_ROOT/client
. ../.venv/bin/activate
python3 encode.py &> ${LOG}
