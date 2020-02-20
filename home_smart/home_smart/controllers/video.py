import sys, time
from datetime import datetime
import numpy as np
import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Response, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor
from .db import get_db
import home_smart

bp = Blueprint('video', __name__)
app = Flask(__name__)

@bp.route('/video')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT d.id AS device_id, d.address, d.name AS device_name, s.id AS sensor_id, s.name AS sensor_name, s.description AS sensor_description '
        'FROM device d '
        'LEFT JOIN sensor s ON d.id = s.device_id '
        'WHERE s.type = \'video\' '
        'ORDER BY s.name ASC'
    )
    cameras = db_cur.fetchall()
    # app.logger.info('sensor name: %s', sensors)
    # return pprint(sensors)
    # app.logger.info('sensor name: %s', sensors.description)
    return render_template('video/index.html', cameras=cameras)