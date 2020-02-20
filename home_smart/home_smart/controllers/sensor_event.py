# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('sensor_event', __name__)
app = Flask(__name__)

@bp.route('/sensor_event')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created FROM sensor_event '
        ' ORDER BY name ASC'
    )
    sensor_events = db_cur.fetchall()
    # app.logger.info('sensor_event name: %s', sensor_events)
    # return pprint(sensor_events)
    # app.logger.info('sensor_event name: %s', sensor_events.description)
    return render_template('sensor_event/index.html', sensor_events=sensor_events)

@bp.route('/sensor_event/create', methods=('GET', 'POST'))
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
                'INSERT INTO sensor_event (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('sensor_event.index'))

    return render_template('sensor_event/create.html')

@bp.route('/sensor_event/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    # robot_state = get_robot_state(id)

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
            db_cur = db.cursor()
            db_cur.execute(
                'UPDATE sensor_event SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('sensor_event.index'))

    sensor_event = get_sensor_event(id)

    return render_template('sensor_event/update.html', sensor_event=sensor_event)

@bp.route('/sensor_event/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    if request.method == 'POST':
        error = None

        if not id:
            error = 'ID is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db_cur = db.cursor()
            db_cur.execute(
                'DELETE FROM sensor_event WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    sensor_event = get_sensor_event(id)

    return redirect(url_for('sensor_event.index'))

def get_sensor_event(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created'
        ' FROM sensor_event'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    sensor_event = db_cur.fetchone()
    if sensor_event is None:
        abort(404, "sensor_event id {0} doesn't exist.".format(id))

    return sensor_event
