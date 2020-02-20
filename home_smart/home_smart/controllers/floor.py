# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, json, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('floor', __name__)
app = Flask(__name__)

@bp.route('/floor')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    query = 'SELECT f.id, f.location_id, f.name, f.description, f.created FROM floor f;'
    db_cur.execute(query)
    floors = db_cur.fetchall()
    db_cur.close()
    pprint('floors: ')
    pprint(floors)
    # app.logger.info('floor name: %s', floors)
    # return pprint(floors)
    # app.logger.info('floor name: %s', floors.description)
    return render_template('floor/index.html', floors=floors)

@bp.route('/floor/create', methods=('GET', 'POST'))
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
                'INSERT INTO floor (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('floor.index'))

    return render_template('floor/create.html')

@bp.route('/floor/<int:id>/update', methods=('GET', 'POST'))
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
                'UPDATE floor SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('floor.index'))

    floor = get_floor(id)

    return render_template('floor/update.html', floor=floor)

@bp.route('/floor/location/<int:id>/', methods=('GET', 'POST'))
def get_by_location_id(id):
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
                'UPDATE floor SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('floor.index'))

    floor = get_floor(id)

    return render_template('floor/update.html', floor=floor)

@bp.route('/floor/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM floor WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    floor = get_floor(id)

    return redirect(url_for('floor.index'))

def get_floor(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created'
        ' FROM floor'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    floor = db_cur.fetchone()
    if floor is None:
        abort(404, "floor id {0} doesn't exist.".format(id))

    return floor
