# Grab video from camera with ffmpeg (plays in Quicktime)
# ffmpeg -f video4linux2 -r 12 -i /dev/video0 -vcodec libx264 -r 12 -pix_fmt yuv420p /var/www/home_smart/home_smart/tmp/out.mp4
import sys, time
from datetime import datetime
# import numpy as np
# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Response, Flask
)
import home_smart
from home_smart.modules.model import Model

bp = Blueprint('sensor', __name__)
app = Flask(__name__)

@bp.route('/sensor')
def index():
    model_sensor = Model('sensor')
    sensors = model_sensor.select_all()
    return render_template('sensor/index.html', sensors=sensors)

@bp.route('/sensor/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db_cur = db.cursor(cursor_factory=RealDictCursor)
            db_cur.execute(
                'INSERT INTO sensor (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('sensor.index'))

    return render_template('sensor/create.html')

@bp.route('/sensor/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    model_sensor = Model('sensor')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        device_id = request.form['device_id']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not device_id:
            error = 'Device ID is required.'

        if error is not None:
            flash(error)
        else:
            sensors = model_sensor.update({'name': name, 'description': description, 'device_id': device_id, 'id': id})
            return redirect(url_for('sensor.index'))

    sensor = model_sensor.select_by_id(id)

    return render_template('sensor/update.html', sensor=sensor)

@bp.route('/sensor/<int:id>', methods=('GET', 'POST'))
def single(id):
    db = get_db()

    with db:
        db_cur = db.cursor(cursor_factory=RealDictCursor)
        db_cur.execute('SELECT id, device_id, INITCAP(CAST(type AS text)) AS type, name, description, created FROM sensor WHERE id = %s', (id,))

    sensor = db_cur.fetchone()

    # capture_video(sensor['id'])

    return render_template('sensor/single.html', sensor=sensor)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/sensor/video-feed/<int:id>', methods=('GET', 'POST'))
def sensor_video_feed(id):
    return Response(gen(home_smart.OpenCvCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(gen(home_smart.FfmpegCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/video-feed', methods=('GET', 'POST'))
def video_feed():
    return Response(gen(home_smart.OpenCvCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def capture_video(sensor_id):
    cap = cv.VideoCapture(0)
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    file_name = '/var/www/home_smart/home_smart/tmp/sensor_' + str(sensor_id) + datetime.now().strftime("_%Y_%m_%d_%H_%M_%S") + '.avi'
    out = cv.VideoWriter(file_name, fourcc, 20.0, (320,  240))
    start = time.time()
    print("time started ...")
    # cap.open()
    while cap.isOpened():
        print("isOpened ...")
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv.flip(frame, 0)
        # write the flipped frame
        out.write(frame)
        # cv.imshow('frame', frame)
        # if cv.waitKey(1) == ord('q'):
        #     break
        end = time.time()
        if (end - start) > (6 * 1): # (sec * min)
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    # cv.destroyAllWindows()

@bp.route('/sensor/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    if request.method == 'POST':
        error = None

        if not id:
            error = 'ID is required.'
        if error is not None:
            flash(error)
        else:
            model_sensor = Model('sensor')
            model_sensor.delete(id)

    return redirect(url_for('sensor.index'))

def get_sensor(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, device_id, created'
        ' FROM sensor'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    sensor = db_cur.fetchone()
    if sensor is None:
        abort(404, "sensor id {0} doesn't exist.".format(id))

    return sensor
