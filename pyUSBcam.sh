FN_L=/home/admin/proj/pyUSBcam/img_l/$DD.jpg
FN_S=/home/admin/proj/pyUSBcam/img_s/current.jpg
count=0
while true
do
  DD=`date '+%Y-%m-%d_%H:%M:%S'`
  /usr/bin/fswebcam 640x480 --jpeg 50 $FN_S
  /usr/bin/python /home/admin/proj/pyUSBcam/encode.py
  count=`echo "$count+1" | bc`
   if [ $count = 5 ]; then
      /usr/bin/fswebcam 640x480 $FN_S
      count=0
  fi
done