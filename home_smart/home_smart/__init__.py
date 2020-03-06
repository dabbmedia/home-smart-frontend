import os, sys
from flask import Flask
from home_smart.controllers import home_smart, db, location, floor, room, device, sensor, sensor_event, actuator, actuator_event, network, video
from home_smart.modules.model import Model
from home_smart.modules.camera.open_cv_camera import OpenCvCamera
# from home_smart.modules.camera.ffmpeg_camera import FfmpegCamera

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from home_smart.controllers import db
    db.init_app(app)

    # from home_smart import device
    # device.init_device(app)

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
    
    return app
