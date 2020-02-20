# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('actuator_event', __name__)
app = Flask(__name__)

@bp.route('/actuator_event')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created FROM actuator_event '
        ' ORDER BY name ASC'
    )
    actuator_events = db_cur.fetchall()
    # app.logger.info('actuator_event name: %s', actuator_events)
    # return pprint(actuator_events)
    # app.logger.info('actuator_event name: %s', actuator_events.description)
    return render_template('actuator_event/index.html', actuator_events=actuator_events)

@bp.route('/actuator_event/create', methods=('GET', 'POST'))
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
                'INSERT INTO actuator_event (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('actuator_event.index'))

    return render_template('actuator_event/create.html')

@bp.route('/actuator_event/<int:id>/update', methods=('GET', 'POST'))
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
                'UPDATE actuator_event SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('actuator_event.index'))

    actuator_event = get_actuator_event(id)

    return render_template('actuator_event/update.html', actuator_event=actuator_event)

@bp.route('/actuator_event/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM actuator_event WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    actuator_event = get_actuator_event(id)

    return redirect(url_for('actuator_event.index'))

def get_actuator_event(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created'
        ' FROM actuator_event'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    actuator_event = db_cur.fetchone()
    if actuator_event is None:
        abort(404, "actuator_event id {0} doesn't exist.".format(id))

    return actuator_event
