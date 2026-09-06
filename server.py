from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/frame', methods=['POST'])
def receive_frame():
    global latest_frame
    latest_frame = request.json.get('image')
    return jsonify({'status': 'ok'})

@app.route('/api/frame', methods=['GET'])
def get_frame():
    return jsonify({'image': latest_frame})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
