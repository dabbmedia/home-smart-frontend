# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('actuator', __name__)
app = Flask(__name__)

@bp.route('/actuator')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created FROM actuator '
        ' ORDER BY name ASC'
    )
    actuators = db_cur.fetchall()
    # app.logger.info('actuator name: %s', actuators)
    # return pprint(actuators)
    # app.logger.info('actuator name: %s', actuators.description)
    return render_template('actuator/index.html', actuators=actuators)

@bp.route('/actuator/create', methods=('GET', 'POST'))
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
                'INSERT INTO actuator (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('actuator.index'))

    return render_template('actuator/create.html')

@bp.route('/actuator/<int:id>/update', methods=('GET', 'POST'))
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
                'UPDATE actuator SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('actuator.index'))

    actuator = get_actuator(id)

    return render_template('actuator/update.html', actuator=actuator)

@bp.route('/actuator/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM actuator WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    actuator = get_actuator(id)

    return redirect(url_for('actuator.index'))

def get_actuator(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created'
        ' FROM actuator'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    actuator = db_cur.fetchone()
    if actuator is None:
        abort(404, "actuator id {0} doesn't exist.".format(id))

    return actuator
