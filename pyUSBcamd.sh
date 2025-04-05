# for service
# Copy to  /etc/systemd/system/pyUSBcam.service
# sudo systemctl daemon-reload
# sudo systemctl enable webcam
LOG=/home/admin/proj/pyUSBcam/log/pyUSBcam.log
sh /home/admin/proj/pyUSBcam/pyUSBcam.sh >> $LOG 2>&1
