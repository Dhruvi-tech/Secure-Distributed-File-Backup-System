from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid
import hashlib
import io
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple file storage (replaces Cassandra for standalone)
STORAGE_DIR = "file_storage"
METADATA_FILE = "files_metadata.json"

os.makedirs(STORAGE_DIR, exist_ok=True)

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, default=str)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_data = file.read()
    file_id = str(uuid.uuid4())
    
    # Save file
    file_path = os.path.join(STORAGE_DIR, file_id)
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    # Save metadata
    metadata = load_metadata()
    metadata[file_id] = {
        'filename': file.filename,
        'file_size': len(file_data),
        'upload_time': datetime.now().isoformat(),
        'checksum': hashlib.md5(file_data).hexdigest()
    }
    save_metadata(metadata)
    
    return jsonify({'file_id': file_id, 'status': 'uploaded'})

@app.route('/download/<file_id>')
def download_file(file_id):
    metadata = load_metadata()
    if file_id not in metadata:
        return jsonify({'error': 'File not found'}), 404
    
    file_path = os.path.join(STORAGE_DIR, file_id)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File data not found'}), 404
    
    return send_file(file_path, as_attachment=True, 
                    download_name=metadata[file_id]['filename'])

@app.route('/files')
def list_files():
    metadata = load_metadata()
    return jsonify([{
        'file_id': file_id,
        'filename': info['filename'],
        'file_size': info['file_size'],
        'upload_time': info['upload_time']
    } for file_id, info in metadata.items()])

@app.route('/')
def home():
    return '''
    <h1>🔐 SDFBS Phase 1 - Standalone Mode</h1>
    <p>✅ Server is running!</p>
    <p><a href="/files">View Files API</a></p>
    <p><a href="http://localhost:3001">Web Interface</a></p>
    '''

if __name__ == '__main__':
    print("🚀 Starting SDFBS Phase 1 Standalone Server...")
    print("📊 API: http://localhost:8080")
    print("🌐 Web: http://localhost:3001")
    app.run(host='0.0.0.0', port=8080, debug=True)