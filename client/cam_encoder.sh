#!/bin/bash
PROJECT_ROOT=/home/admin/pyUSBcam
TS=$(date "+%Y%m%d%H%M%S")
LOG=${PROJECT_ROOT}/log/${TS}-encoder.log
# shellcheck disable=SC2164
cd ${PROJECT_ROOT}/client
. ../.venv/bin/activate
python3 encoder.py &> ${LOG}
