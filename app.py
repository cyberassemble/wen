from flask import Flask, render_template, session, redirect, request
from database import conn

app = Flask(__name__)
app.secret_key = 'CXCRACK'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/checker')
def checker():
    if session.get('accses') is None:
        return ('/')

    return render_template('sk_based.html')
    
@app.route('/admin')
def admin():
    passw = request.args.get('passw')

    if passw != 'secret_key':
        return redirect('/')
    
    all = conn.all()
    return render_template('dashboard.html', keys=all)

from blueprints.api import api
from blueprints.sk_based import sk

app.register_blueprint(api)
app.register_blueprint(sk)

app.run(debug=True, port=5000)
