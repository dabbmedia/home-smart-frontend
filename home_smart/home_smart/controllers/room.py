from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from home_smart.modules.model import Model

bp = Blueprint('room', __name__)
app = Flask(__name__)

@bp.route('/room')
def index():
    model_room = Model('room')
    rooms = model_room.select_all()
    return render_template('room/index.html', rooms=rooms)

@bp.route('/room/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        floor_id = request.form['floor_id']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not floor_id:
            error = 'Floor is required.'

        if error is not None:
            flash(error)
        else:
            model_room = Model('room')
            insert_id = model_room.insert({'name': name, 'description': description, 'floor_id': floor_id})
            return redirect(url_for('room.index'))

    model_floor = Model('floor')
    floors = model_floor.select_all()

    return render_template('room/create.html', floors=floors)

@bp.route('/room/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    model_room = Model('room')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        floor_id = request.form['floor_id']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not floor_id:
            error = 'Floor is required.'

        if error is not None:
            flash(error)
        else:
            model_room.update({'name': name, 'description': description, 'floor_id': floor_id, 'id': id})

    room = model_room.select_by_id(id)

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
            model_room = Model('room')
            model_room.delete({'id': id})

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
