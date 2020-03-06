import sys
sys.path.insert(0, '/var/www/home_smart_device')
sys.path.append('/var/www/home_smart_device/home_smart_device/controllers')
# for OpenBSD
sys.path.append('/usr/local/lib/python3.6/site-packages')
#from home_smart_device import app as application
from home_smart_device import create_app
application = create_app()