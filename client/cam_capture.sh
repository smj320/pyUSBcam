#!/bin/bash
PROJECT_ROOT=/home/admin/pyUSBcap
LOG=$PROJECT_ROOT/log
TS=$(date "+%Y%m%d%H%M%S")
# shellcheck disable=SC2164
cd $PROJECT_ROOT/client
find img -name '*.jpg' -delete  > $LOG/$TS-capture.log
find sent -name '*.jpg' -delete  >> $LOG/$TS-capture.log
. ../.venv/bin/activate
python3 capture.py >> $LOG/$TS-capture.log
