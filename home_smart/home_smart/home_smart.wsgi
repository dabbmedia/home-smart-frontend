##uwsgi -s /tmp/home_smart.sock --plugin python3 --processes 4 --threads 2 --manage-script-name --mount __init__:app --thunder-lock
import sys
sys.path.insert(0, '/var/www/home_smart/home_smart/')
from home_smart import app as application
#from home_smart import application
#from home_smart import create_app
#application = create_app()
