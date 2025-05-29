#!/bin/bash
PROJECT_ROOT=/home/admin/pyUSBcam
TS=$(date "+%Y%m%d%H%M%S")
LOG=${PROJECT_ROOT}/log/${TS}-capture.log
# shellcheck disable=SC2164
cd ${PROJECT_ROOT}/client
. ../.venv/bin/activate
if [ "$1" == "-v" ]; then
  python3 capture.py
else
  python3 capture.py &>> ${LOG}
fi