import os, sys
from flask import Flask
import logging
from controllers import home_smart, db, location, floor, room, device, sensor, sensor_event, actuator, actuator_event, network, video

def create_app(test_config=None):
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

    return app

application = create_app
