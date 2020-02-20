import sys
sys.path.insert(0, '/var/www/home_smart_device/')
#from home_smart_device import app as application
from home_smart_device import create_app
application = create_app()