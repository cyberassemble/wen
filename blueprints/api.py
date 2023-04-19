from flask import Blueprint, jsonify, request, session, redirect
from database import conn, Query
from datetime import datetime

import secrets

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello World'})

@api.route('/accses', methods=['POST'])
def accses():
    accses = request.form['accses']
    data = conn.search(Query.accses == accses)[0]

    if datetime.strptime(data['expires'], '%Y-%m-%d') < datetime.now():
        return jsonify({'message': 'Expired'})

    session['accses'] = accses
    session['expires'] = data['expires']

    return redirect('/checker')

@api.route('/create', methods=['POST'])
def create():
    data = request.form
    
    admin_secret = data['admin_secret']
    date = data['date']

    if admin_secret != 'secret_key':
        return jsonify({'message': 'Invalid admin secret'})
    
    secret_key = secrets.token_hex(6)
    
    conn.insert({
        "accses": ("ARTY_" + secret_key.upper()),
        "expires": date
    })

    return redirect('/admin?passw=secret_key')
