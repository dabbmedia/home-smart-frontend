# import cv2 as cv
from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from pprint import pprint
from psycopg2.extras import RealDictCursor

from .db import get_db

bp = Blueprint('network', __name__)
app = Flask(__name__)

@bp.route('/network')
def index():
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created FROM network '
        ' ORDER BY name ASC'
    )
    networks = db_cur.fetchall()
    # app.logger.info('network name: %s', networks)
    # return pprint(networks)
    # app.logger.info('network name: %s', networks.description)
    return render_template('network/index.html', networks=networks)

@bp.route('/network/create', methods=('GET', 'POST'))
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
                'INSERT INTO network (name, description) VALUES (%s, %s)',
                (name, description)
            )
            db.commit()
            return redirect(url_for('network.index'))

    return render_template('network/create.html')

@bp.route('/network/<int:id>/update', methods=('GET', 'POST'))
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
                'UPDATE network SET name = %s, description = %s'
                ' WHERE id = %s',
                (name, description, id)
            )
            db.commit()
            return redirect(url_for('network.index'))

    network = get_network(id)

    return render_template('network/update.html', network=network)

@bp.route('/network/<int:id>/delete', methods=('GET', 'POST'))
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
                'DELETE FROM network WHERE id = %s LIMIT 1',
                (id,)
            )
            db.commit()

    network = get_network(id)

    return redirect(url_for('network.index'))

def get_network(id):
    db = get_db()
    db_cur = db.cursor(cursor_factory=RealDictCursor)
    db_cur.execute(
        'SELECT id, name, description, created'
        ' FROM network'
        ' WHERE id = %s'
        ' ORDER BY name ASC',
        (id,)
    )
    network = db_cur.fetchone()
    if network is None:
        abort(404, "network id {0} doesn't exist.".format(id))

    return network
