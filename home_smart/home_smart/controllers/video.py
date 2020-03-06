from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Response, Flask
)
from psycopg2.extras import RealDictCursor
from .db import get_db
# import home_smart

bp = Blueprint('video', __name__)
app = Flask(__name__)

@bp.route('/video')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT '
        'd.id AS device_id, '
        'd.address, '
        'd.name AS device_name, '
        's.id AS sensor_id, '
        's.name AS sensor_name, '
        's.description AS sensor_description '
        'FROM sensor s '
        'LEFT JOIN device d ON s.device_id = d.id '
        'WHERE s.type = \'video\' '
        'ORDER BY s.name ASC'
    )

    cameras = db_cur.fetchall()

    for camera in cameras:
        print(str(camera['sensor_id']) + ': ' + camera['sensor_name'] + ' - device - ' + str(camera['device_id']) + ': ' + camera['device_name'])
    
    return render_template('video/index.html', cameras=cameras)