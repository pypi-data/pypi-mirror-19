import os

from flask import Flask, render_template, url_for, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask.ext.bower import Bower

from .triggers import triggers_as_dict
from .finders import find_static_asset_dirname

app = Flask(__name__)
app.config.from_object('counter_caller.default_settings')
app.config.from_pyfile(os.path.join(os.getcwd(), 'settings.py'), silent=True)
app.config.from_envvar('COUNTER_CALLER_SETTINGS', silent=True)

sock  = SocketIO(app)
bower = Bower(app)

triggers_dict = triggers_as_dict(app.config['TRIGGERS'])

static_asset_paths = [
    os.getcwd(),
    os.path.join(os.path.dirname(__file__), 'static'),
]

def triggers():
    return triggers_dict

@app.route('/static/<path>')
def find_static(path):
    dirname = find_static_asset_dirname(static_asset_paths, path)

    return send_from_directory(dirname, path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/help')
def help():
    return render_template('help.html', triggers=triggers())

@app.route('/config.json')
def config():
    return jsonify(triggers=triggers(), please_wait=app.config['PLEASE_WAIT'])

@app.route('/triggers/<trigger_id>', methods=['POST'])
def action_trigger(trigger_id):
    sock.emit('queue', trigger_id, broadcast=True)
    return ('', 204)

@app.route('/actions/refresh', methods=['POST'])
def action_refresh():
    sock.emit('refresh', broadcast=True)
    return ('', 204)

@app.route('/actions/clear', methods=['POST'])
def action_clear():
    sock.emit('clear', broadcast=True)
    return ('', 204)

@sock.on('queue')
def queue(trigger_id):
    action_trigger(trigger_id)

@sock.on('refresh')
def refresh():
    action_refresh()

@sock.on('clear')
def clear():
    action_clear()
