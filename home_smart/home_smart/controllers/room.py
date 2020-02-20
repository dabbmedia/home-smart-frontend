# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('room', __name__)
app = Flask(__name__)

@bp.route('/room')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created FROM room '
        ' ORDER BY name ASC'
    )
    rooms = db_cur.fetchall()
    # app.logger.info('room name: %s', rooms)
    # return pprint(rooms)
    # app.logger.info('room name: %s', rooms.description)
    return render_template('room/index.html', rooms=rooms)

@bp.route('/room/create', methods=('GET', 'POST'))
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
                'INSERT INTO room (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('room.index'))

    return render_template('room/create.html')

@bp.route('/room/<int:id>/update', methods=('GET', 'POST'))
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
                'UPDATE room SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('room.index'))

    room = get_room(id)

    return render_template('room/update.html', room=room)

@bp.route('/room/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM room WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    room = get_room(id)

    return redirect(url_for('room.index'))

def get_room(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created'
        ' FROM room'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    room = db_cur.fetchone()
    if room is None:
        abort(404, "room id {0} doesn't exist.".format(id))

    return room
