##uwsgi -s /tmp/home_smart.sock --plugin python3 --processes 4 --threads 2 --manage-script-name --mount __init__:app --thunder-lock
import sys
sys.path.insert(0, '/var/www/home_smart/home_smart/')
#sys.path.append('/var/www/home_smart_device/home_smart_device/controllers')
# for OpenBSD
#sys.path.append('/usr/local/lib/python3.6/site-packages')
from home_smart import app as application
