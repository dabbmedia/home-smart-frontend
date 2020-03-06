from flask import (
    Blueprint, jsonify, redirect, render_template, request, url_for, Flask
)
from home_smart.modules.model import Model

bp = Blueprint('network', __name__)
app = Flask(__name__)

@bp.route('/network')
def index():
    model_network = Model('network')
    networks = model_network.select_all()
    return render_template('network/index.html', networks=networks)

@bp.route('/network/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location_id = request.form['location_id']
        public_address = request.form['public_address']
        gateway_address = request.form['gateway_address']
        subnet_address = request.form['subnet_address']
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not location_id:
            error = 'Location is required.'
        if not public_address:
            error = 'Public Address is required.'
        if not gateway_address:
            error = 'Gateway Address is required.'
        if not subnet_address:
            error = 'Subnet Address is required.'

        if error is not None:
            flash(error)
        else:
            model_network = Model('network')
            insert_id = model_network.insert({
                'name': name, 
                'description': description, 
                'location_id': location_id, 
                'public_address': public_address, 
                'gateway_address': gateway_address, 
                'subnet_address': subnet_address
            })
            return redirect(url_for('network.index'))

    model_location = Model('location')
    locations = model_location.select_all()

    return render_template('network/create.html', locations=locations)

@bp.route('/network/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    model_network = Model('network')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if not location_id:
            error = 'Location is required.'
        if not public_address:
            error = 'Public Address is required.'
        error = None

        if not name:
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'
        if not location_id:
            error = 'Location is required.'
        if not public_address:
            error = 'Public Address is required.'
        if not gateway_address:
            error = 'Gateway Address is required.'
        if not subnet_address:
            error = 'Subnet Address is required.'

        if error is not None:
            flash(error)
        else:
            model_network.update({
                'name': name, 
                'description': description, 
                'location_id': location_id, 
                'public_address': public_address, 
                'gateway_address': gateway_address, 
                'subnet_address': subnet_address
            })
            return redirect(url_for('network.index'))

    model_location = Model('location')
    locations = model_location.select_all()

    network = model_network.select_by_id(id)
    network['locations'] = locations

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
