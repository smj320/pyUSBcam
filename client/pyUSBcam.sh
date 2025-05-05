#!/bin/zsh
PROJECT_ROOT=/home/admin/pyUSBcam
# PROJECT_ROOT=/Users/kikuchi/Projects/PycharmProjects/pyUSBcam
LOG=$PROJECT_ROOT/log
TS=$(date "+%Y%m%d%H%M%S")
# shellcheck disable=SC2164
echo $PROJECT_ROOT/client
# shellcheck disable=SC2164
cd $PROJECT_ROOT/client
find img -name '*.jpg' -delete  > $LOG/$TS-client.log
find sent -name '*.jpg' -delete  >> $LOG/$TS-client.log
. ../.venv/bin/activate
python3 capture.py > $LOG/$TS-capture.log &
# sleep 5
python3 encoder.py >> $LOG/$TS-client.log
