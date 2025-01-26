import os
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='dist', static_url_path='/')

@app.route('/api/hello')
def api_hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join('dist', path)):
        return send_from_directory('dist', path)
    else:
        return send_from_directory('dist', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
