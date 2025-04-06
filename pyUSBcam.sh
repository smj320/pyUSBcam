while true
do
  DD=`date '+%Y-%m-%d_%H:%M:%S'`
  FN_L=/home/admin/proj/pyUSBcam/img_l/$DD.jpg
  FN_S=/home/admin/proj/pyUSBcam/img_s/current.jpg
  /usr/bin/fswebcam 640x480 --jpeg 50 $FN_L
  /usr/bin/fswebcam 640x480 --jpeg 50 $FN_S
  /usr/bin/python /home/admin/proj/pyUSBcam/encode.py
done