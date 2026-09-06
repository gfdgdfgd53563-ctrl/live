from flask import Flask, jsonify, request
import os

app = Flask(__name__)
latest_frame = None

@app.route('/')
def home():
    return '<h1>PCBot Live Server ✓</h1><p>En attente de frames...</p>'

@app.route('/api/frame', methods=['POST'])
def receive_frame():
    global latest_frame
    try:
        data = request.get_json() or {}
        latest_frame = data.get('image')
        return jsonify({'status': 'ok'})
    except:
        return jsonify({'status': 'error'})

@app.route('/api/frame', methods=['GET'])
def get_frame():
    return jsonify({'image': latest_frame})

if __name__ == '__main__':
    app.run()
