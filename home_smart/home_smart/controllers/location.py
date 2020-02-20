# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
import json
from pprint import pprint
# from __future__ import print_function
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('location', __name__)
app = Flask(__name__)

@bp.route('/location')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created '
        'FROM location '
        ' ORDER BY name ASC'
    )
    locations = db_cur.fetchall()
    pprint('locations: ')
    pprint(locations)
    # app.logger.info('location name: %s', locations)
    # return pprint(locations)
    # app.logger.info('location name: %s', locations.description)
    return render_template('location/index.html', locations=locations)

@bp.route('/location/create', methods=('GET', 'POST'))
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
            db_cur = db.cursor()
            db_cur.execute(
                'INSERT INTO location (name, description) VALUES (%s, %s)',
                (name, description)
            )
            location_id = db_cur.fetchone()[0]
            db_cur.execute(
                'INSERT INTO floor (location_id, name, description) VALUES (%s, %s)',
                (location_id, name, description)
            )
            floor_id = db_cur.fetchone()[0]
            db_cur.execute(
                'INSERT INTO room (floor_id, name, description) VALUES (%s, %s)',
                (floor_id, name, description)
            )
            db.commit()
            return redirect(url_for('location.index'))

    return render_template('location/create.html')

@bp.route('/location/<int:id>', methods=('GET', 'POST'))
def single(id):
    location = get_location(id)

    return render_template('location/single.html', location=location)

@bp.route('/location/<int:id>/update', methods=('GET', 'POST'))
def update(id):
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
                'UPDATE location SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            # return redirect(url_for('location.update', id=location['id']))

    location_floors = get_location(id)

    return render_template('location/update.html', location_floors=location_floors)

@bp.route('/location/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM location WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    location = get_location(id)

    return redirect(url_for('location.index'))

def get_location(id):
    db = get_db()
    with db:
        db_cur = db.cursor(cursor_factory=RealDictCursor)
        db_cur.execute(
            'SELECT '
              'l.id, l.name, l.description, l.created '
              'FROM location l '
              'WHERE l.id = %s '
              'ORDER BY l.name ASC',
            (id,)
        )
        
        location = db_cur.fetchone()

        if location is None:
            abort(404, "locations not found.".format(id))

    #     app.logger.debug('location json: %s', location_json)
    floors = get_location_floors(location['id'])
    location['floors'] = floors

    return location

def get_location_floors(location_id):
    pprint(location_id)
    db = get_db()
    with db:
        db_cur = db.cursor(cursor_factory=RealDictCursor)
        sql = 'SELECT f.id, f.location_id, f.name, f.created FROM floor f WHERE f.location_id = %s ORDER BY f.name;'
        db_cur.execute(sql, (location_id,))
        floors = db_cur.fetchall()

    for floor in floors:
        rooms = get_floor_rooms(floor['id'])
        floor['rooms'] = rooms

    return floors

def get_floor_rooms(floor_id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute('SELECT id, name FROM room WHERE floor_id = %s ORDER BY name', (floor_id,))
    rooms = db_cur.fetchall()
    for room in rooms:
        devices = get_room_devices(room['id'])
        room['devices'] = devices
    return rooms

def get_room_devices(room_id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute('SELECT id, name FROM device WHERE room_id = %s ORDER BY name', (room_id,))
    devices = db_cur.fetchall()
    for device in devices:
        sensors = get_device_sensors(device['id'])
        device['sensors'] = sensors
    return devices

def get_device_sensors(device_id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute('SELECT id, name FROM sensor WHERE device_id = %s ORDER BY name', (device_id,))
    sensors = db_cur.fetchall()
    return sensors

def get_sensor_sensor_events(sensor_id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute('SELECT id, name FROM sensor_event WHERE sensor_id = %s ORDER BY name', (sensor_id,))
    sensor_events = db_cur.fetchall()
    return sensor_events

def get_device_actuators(device_id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute('SELECT id, name FROM actuator WHERE device_id = %s ORDER BY name', (device_id,))
    actuators = db_cur.fetchall()
    return actuators

def get_sensor_actuator_events(actuator_id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute('SELECT id, name FROM actuator_event WHERE actuator_id = %s ORDER BY name', (actuator_id,))
    actuator_events = db_cur.fetchall()
    return actuator_events
