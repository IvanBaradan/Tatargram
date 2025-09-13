from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Serve files from the current directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("Server running at http://localhost:8000/")
    app.run(host='127.0.0.1', port=8000, debug=True)