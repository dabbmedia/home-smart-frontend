import sys
sys.path.insert(0, '/var/www/home_smart/')
#from home_smart import app as application
from home_smart import create_app
application = create_app()