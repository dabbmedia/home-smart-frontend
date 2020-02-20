# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('device', __name__)
app = Flask(__name__)

@bp.route('/device')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, address, created FROM device '
        ' ORDER BY name ASC'
    )
    devices = db_cur.fetchall()
    # app.logger.info('device name: %s', devices)
    # return pprint(devices)
    # app.logger.info('device name: %s', devices.description)
    return render_template('device/index.html', devices=devices)

@bp.route('/device/create', methods=('GET', 'POST'))
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
                'INSERT INTO device (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('device.index'))

    return render_template('device/create.html')

@bp.route('/device/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        address = request.form['address']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not address:
            error = 'Address is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db_cur = db.cursor()
            db_cur.execute(
                'UPDATE device SET name = %s, description = %s, address = %s'
                ' WHERE id = %s',
                (name, description, address, id)
            )
            db.commit()
            return redirect(url_for('device.index'))

    device = get_device(id)

    return render_template('device/update.html', device=device)

@bp.route('/device/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM device WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    device = get_device(id)

    return redirect(url_for('device.index'))

def get_device(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, address, created'
        ' FROM device'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    device = db_cur.fetchone()
    if device is None:
        abort(404, "device id {0} doesn't exist.".format(id))

    return device
