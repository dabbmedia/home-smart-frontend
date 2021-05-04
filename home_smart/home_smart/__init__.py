# uwsgi -s /tmp/home_smart.sock --manage-script-name --mount /home_smart=home_smart:app
# uwsgi -s /tmp/home_smart.sock --plugin python3 --processes 4 --threads 2 --manage-script-name --mount /home_smart/__init__=create_app:app --thunder-lock
# uwsgi -s /tmp/home_smart.sock --plugin python3 --wsgi-file home_smart/__init__.py --callable create_app --processes 4 --threads 2 --thunder-lock
# uwsgi --socket 127.0.0.1:3031 --plugin python3 --wsgi-file home_smart/__init__.py --callable create_app --processes 4 --threads 2 --stats 127.0.0.1:9191
import os, sys
from flask import Flask
import logging
from controllers import home_smart, db, location, floor, room, device, sensor, sensor_event, actuator, actuator_event, network, video
# from controllers import db, home_smart, location, floor, room, device, sensor, sensor_event, actuator, actuator_event, network, video
# from modules.model import Model
# from modules.camera.open_cv_camera import OpenCvCamera
# from home_smart.modules.camera.ffmpeg_camera import FfmpegCamera

# def create_app(test_config=None):
# def create_app(pid=0, app=app, req="1/1", test_config=None):
#     """Create and configure an instance of the Flask application."""
#     app = Flask(__name__, instance_relative_config=True)
#     print('app instantiated')
    # app.config.from_mapping(
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY='dev',
    # )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.update(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     from controllers import db
#     db.init_app(app)

#     # from home_smart import device
#     # device.init_device(app)

#     @app.route("/hello")
#     def hello():
#         print('hello-ing')
#         return "Hello, World!"

#     # app.register_blueprint(home_smart.bp)
#     # app.register_blueprint(location.bp)
#     # app.register_blueprint(floor.bp)
#     # app.register_blueprint(room.bp)
#     # app.register_blueprint(device.bp)
#     # app.register_blueprint(sensor.bp)
#     # app.register_blueprint(sensor_event.bp)
#     # app.register_blueprint(actuator.bp)
#     # app.register_blueprint(actuator_event.bp)
#     # app.register_blueprint(network.bp)
#     # app.register_blueprint(video.bp)
#     # app.add_url_rule('/', endpoint='index')

#     print('blueprints registered')
    
#     return app
app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY='dev',
)

logging.basicConfig(filename='home_smart.log', level=logging.DEBUG)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from controllers import db
db.init_app(app)

app.register_blueprint(home_smart.bp)
app.register_blueprint(location.bp)
app.register_blueprint(floor.bp)
app.register_blueprint(room.bp)
app.register_blueprint(device.bp)
app.register_blueprint(sensor.bp)
app.register_blueprint(sensor_event.bp)
app.register_blueprint(actuator.bp)
app.register_blueprint(actuator_event.bp)
app.register_blueprint(network.bp)
app.register_blueprint(video.bp)
app.add_url_rule('/', endpoint='index')

# uwsgi expects "application" by default
application = app
