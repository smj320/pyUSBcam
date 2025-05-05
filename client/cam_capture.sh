#!/bin/bash
PROJECT_ROOT=/home/admin/pyUSBcap
TS=$(date "+%Y%m%d%H%M%S")
LOG=${PROJECT_ROOT}/log/${TS}-capture.log
# shellcheck disable=SC2164
cd ${PROJECT_ROOT}/client
find img -name '*.jpg' -delete  &> ${LOG}
find sent -name '*.jpg' -delete  &>> ${LOG}
. ../.venv/bin/activate
python3 capture.py &>> ${LOG}
