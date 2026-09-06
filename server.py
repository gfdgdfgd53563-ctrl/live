from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

current_client = None
latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global current_client
    current_client = request.sid
    emit('status', {'data': 'Connecté au serveur'})
    if latest_frame:
        emit('frame', {'image': latest_frame})

@socketio.on('send_frame')
def handle_frame(data):
    global latest_frame
    latest_frame = data.get('image')
    socketio.emit('frame', {'image': latest_frame})

@socketio.on('mouse_move')
def handle_mouse_move(data):
    socketio.emit('mouse_event', {'type': 'move', 'x': data['x'], 'y': data['y']}, to=current_client)

@socketio.on('mouse_click')
def handle_click(data):
    socketio.emit('mouse_event', {'type': 'click', 'button': data.get('button', 'left')}, to=current_client)

@socketio.on('key_press')
def handle_key(data):
    socketio.emit('key_event', {'type': 'press', 'key': data['key']}, to=current_client)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
