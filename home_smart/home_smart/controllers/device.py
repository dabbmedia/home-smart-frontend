from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from psycopg2.extras import RealDictCursor

from  modules.model import Model

bp = Blueprint('device', __name__)
app = Flask(__name__)

@bp.route('/device')
def index():
    model_device = Model('device')
    devices = model_device.select_all()
    return render_template('device/index.html', devices=devices)

@bp.route('/device/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        room_id = request.form['room_id']
        name = request.form['name']
        description = request.form['description']
        address = request.form['address']
        error = None

        if not room_id:
            error = 'Room ID is required.'
        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not address:
            error = 'IP Address/URL is required.'
        if error is not None:
            flash(error)
        else:
            model_device = Model('device')
            insert_id = model_device.insert({'room_id': room_id, 'name': name, 'description': description, 'address': address})
            return redirect(url_for('device.index'))
    
    model_room = Model('room')
    rooms = model_room.select_all()
    # app.logger.info('/device/create rooms retrieved')

    return render_template('device/create.html', rooms=rooms)

@bp.route('/device/<int:id>', methods=('GET', 'POST'))
def single(id):
    model_device = Model('device')
    device = model_device.select_by_id(id)
    return render_template('device/single.html', device=device)

@bp.route('/device/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    model_device = Model('device')
    if request.method == 'POST':
        room_id = request.form['room_id']
        name = request.form['name']
        description = request.form['description']
        address = request.form['address']
        error = None

        if not room_id:
            error = 'Room ID is required.'
        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not address:
            error = 'Address is required.'

        if error is not None:
            flash(error)
        else:
            model_device.update({'room_id': room_id, 'name': name, 'description': description, 'address': address, 'id': id})
            return redirect(url_for('device.index'))

    device = model_device.select_by_id(id)

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
            model_device = Model('device')
            model_device.delete(id)

    return redirect(url_for('device.index'))
