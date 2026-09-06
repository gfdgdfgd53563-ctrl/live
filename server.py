from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from PIL import ImageGrab
import base64
import io
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

streaming = False
current_client = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global current_client
    current_client = request.sid
    emit('status', {'data': 'Connecté au serveur'})

@socketio.on('start_stream')
def start_stream():
    global streaming
    streaming = True
    threading.Thread(target=stream_screen, daemon=True).start()

def stream_screen():
    global streaming
    while streaming:
        try:
            img = ImageGrab.grab()
            img.thumbnail((1280, 720))
            
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=60)
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            socketio.emit('frame', {'image': img_base64}, to=current_client)
            time.sleep(0.1)
        except Exception as e:
            print(f"Erreur stream: {e}")

@socketio.on('mouse_move')
def handle_mouse_move(data):
    x, y = data['x'], data['y']
    # Code pour bouger la souris
    import pyautogui
    pyautogui.moveTo(x, y, duration=0)

@socketio.on('click')
def handle_click(data):
    import pyautogui
    pyautogui.click()

@socketio.on('disconnect')
def handle_disconnect():
    global streaming
    streaming = False

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
Fichier 2 : requirements.txt


Flask==2.3.0
flask-socketio==5.3.0
python-socketio==5.9.0
Pillow==10.0.0
pyautogui==0.9.53