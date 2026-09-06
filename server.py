from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('status', {'connected': True})

@socketio.on('send_frame')
def handle_frame(data):
    global latest_frame
    latest_frame = data.get('image')
    socketio.emit('frame', {'image': latest_frame}, broadcast=True)

@socketio.on('mouse_move')
def handle_mouse(data):
    socketio.emit('mouse_event', data, broadcast=True)

@socketio.on('mouse_click')
def handle_click(data):
    socketio.emit('click_event', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
