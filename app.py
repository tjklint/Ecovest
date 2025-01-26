from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='dist', static_url_path='/dist')

# Example API route
@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})

# Serve the main page at '/'
@app.route('/')
def serve_main():
    return send_from_directory('dist', 'index.html')

# Serve the analytics page at '/analytics'
@app.route('/analytics')
def serve_analytics():
    return send_from_directory('dist', 'analytics.html')

# OPTIONAL: If you have additional static files in dist/assets, you can add:
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('dist/assets', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
