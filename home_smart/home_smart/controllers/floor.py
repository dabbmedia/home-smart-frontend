from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, json, Flask
)

from modules.floor import Floor

bp = Blueprint('floor', __name__)
app = Flask(__name__)

@bp.route('/floor')
def index():
    floor = Floor()
    floors = floor.get_floors()
    return render_template('floor/index.html', floors=floors)

@bp.route('/floor/<int:id>', methods=('GET', 'POST'))
def single(id):
    model_floor = Model('floor')
    floor = model_floor.select_by_id(id)
    
    return render_template('floor/single.html', floor=floor)

@bp.route('/floor/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location_id = request.form['location_id']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not location_id:
            error = 'Location is required.'

        if error is not None:
            flash(error)
        else:
            model_floor = Model('floor')
            insert_id = model_floor.insert({'name': name, 'description': description, 'location_id': location_id})

            return redirect(url_for('floor.index'))

    model_location = Model('location')
    locations = model_location.select_all()

    return render_template('floor/create.html', locations=locations)

@bp.route('/floor/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    floor = Floor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location_id = request.form['location_id']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not location_id:
            error = 'Location is required.'

        if error is not None:
            flash(error)
        else:
            floor.update({'name': name, 'description': description, 'location_id': location_id, 'id': id})

    floor = floor.get_floor(id)

    return render_template('floor/update.html', floor=floor)

@bp.route('/floor/location/<int:id>/', methods=('GET', 'POST'))
def get_by_location_id(id):
    model_floor = Model('floor')
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

    floor = model_floor.select_by_id(id)

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
            floor = Floor()
            floor.delete(id)

    return redirect(url_for('floor.index'))
