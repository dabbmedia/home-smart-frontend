import os, sys
from flask import Flask
print(sys.path)
from home_smart_device.controllers import home_smart_device
from home_smart_device.modules.camera.open_cv_camera import OpenCvCamera
# from home_smart_device.modules.camera.ffmpeg_camera import FfmpegCamera

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        # DATABASE=os.path.join(app.instance_path, 'home_smart_device.sqlite'),
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

    # from home_smart_device.controllers import db
    # db.init_app(app)

    # from home_smart_device import device
    # device.init_device(app)

    app.register_blueprint(home_smart_device.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
