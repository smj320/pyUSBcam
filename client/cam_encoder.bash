#!/bin/bash
# shellcheck disable=SC1073
# Captureが立ち上がるのを待つ
if [ "$1" == "-v" ]; then
  echo "Verbose mode"
else
  sleep 60
fi

PROJECT_ROOT=/home/admin/pyUSBcam
TS=$(date "+%Y%m%d%H%M%S")
LOG=${PROJECT_ROOT}/log/${TS}-encoder.log
# shellcheck disable=SC2164
cd ${PROJECT_ROOT}/client
. ../.venv/bin/activate
if [ "$1" == "-v" ]; then
  python3 encoder.py
else
  python3 encoder.py &> ${LOG}
fi

