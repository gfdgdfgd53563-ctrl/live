from flask import Flask, jsonify, request
import os

app = Flask(__name__)
latest_frame = None

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>PCBot Live</title>
        <style>
            body { margin: 0; padding: 0; background: #000; color: white; font-family: Arial; }
            canvas { display: block; max-width: 100%; }
        </style>
    </head>
    <body>
        <canvas id="screen"></canvas>
        <script>
            const canvas = document.getElementById('screen');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0f0';
            ctx.font = '20px Arial';
            ctx.fillText('En attente de connexion...', 50, 50);
        </script>
    </body>
    </html>
    '''

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
