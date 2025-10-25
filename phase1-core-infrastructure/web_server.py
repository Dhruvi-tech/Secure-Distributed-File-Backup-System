from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve_web():
    return send_from_directory('web', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('web', filename)

if __name__ == '__main__':
    print("🌐 Starting Web Interface Server...")
    print("📱 Access: http://localhost:3001")
    app.run(host='0.0.0.0', port=3001, debug=True)