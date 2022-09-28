#! /bin/sh
# /etc/init.d/home_smart_device
#

# Some things that run always
touch /var/lock/home_smart_device
chmod -Rf 0777 /dev/video0

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting script home_smart_device "
    python3 /var/www/home_smart_device/start_motion_detection.py
    ;;
  stop)
    echo "Stopping script home_smart_device"
    echo "Could do more here"
    ;;
  *)
    echo "Usage: /etc/init.d/home_smart_device {start|stop}"
    exit 1
    ;;
esac

exit 0