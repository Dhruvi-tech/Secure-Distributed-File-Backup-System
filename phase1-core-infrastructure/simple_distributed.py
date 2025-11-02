from flask import Flask, request, jsonify, render_template_string
import uuid
import hashlib
import os
import json
from datetime import datetime

app = Flask(__name__)

STORAGE_DIR = "distributed_files"
CHUNK_SIZE = 1024 * 1024  # 1MB
os.makedirs(STORAGE_DIR, exist_ok=True)

file_metadata = {}

def chunk_file(file_data):
    chunks = []
    for i in range(0, len(file_data), CHUNK_SIZE):
        chunk = file_data[i:i + CHUNK_SIZE]
        chunk_id = hashlib.md5(chunk).hexdigest()
        chunks.append({
            'id': chunk_id,
            'data': chunk,
            'index': len(chunks)
        })
    return chunks

def save_chunk(chunk_id, data):
    path = os.path.join(STORAGE_DIR, chunk_id)
    with open(path, 'wb') as f:
        f.write(data)

def load_chunk(chunk_id):
    path = os.path.join(STORAGE_DIR, chunk_id)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    return None

WEB_INTERFACE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SDFBS - Distributed File Backup</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .box { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 3px; cursor: pointer; }
        .file { background: white; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat { background: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Secure Distributed File Backup System</h1>
        <p>Phase 1: File Chunking & Distributed Storage</p>
    </div>

    <div class="stats">
        <div class="stat">
            <h3>{{ file_count }}</h3>
            <p>Files Stored</p>
        </div>
        <div class="stat">
            <h3>{{ chunk_count }}</h3>
            <p>Total Chunks</p>
        </div>
        <div class="stat">
            <h3>Online</h3>
            <p>System Status</p>
        </div>
    </div>

    <div class="box">
        <h3>Upload File to Distributed Storage</h3>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" id="fileInput" required>
            <button type="submit">Upload & Chunk File</button>
        </form>
        <div id="uploadStatus"></div>
    </div>

    <div class="box">
        <h3>Distributed Files</h3>
        {% for file_id, info in files.items() %}
        <div class="file">
            <strong>{{ info.filename }}</strong> ({{ info.size }} bytes)
            <br><small>{{ info.chunk_count }} chunks | Uploaded: {{ info.upload_time }}</small>
            <a href="/download/{{ file_id }}" style="float: right;">Download</a>
        </div>
        {% endfor %}
    </div>

    <script>
        document.getElementById('uploadForm').onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('file', document.getElementById('fileInput').files[0]);
            
            document.getElementById('uploadStatus').innerHTML = 'Chunking and storing file...';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('uploadStatus').innerHTML = 'Error: ' + data.error;
                } else {
                    document.getElementById('uploadStatus').innerHTML = 
                        `Success! File split into ${data.chunks} chunks and stored.`;
                    setTimeout(() => location.reload(), 2000);
                }
            });
        };
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    chunk_count = len(os.listdir(STORAGE_DIR))
    return render_template_string(WEB_INTERFACE, 
                                files=file_metadata,
                                file_count=len(file_metadata),
                                chunk_count=chunk_count)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    
    file_data = file.read()
    file_id = str(uuid.uuid4())
    
    # Chunk the file
    chunks = chunk_file(file_data)
    
    # Store chunks
    for chunk in chunks:
        save_chunk(chunk['id'], chunk['data'])
    
    # Save metadata
    file_metadata[file_id] = {
        'filename': file.filename,
        'size': len(file_data),
        'chunk_count': len(chunks),
        'chunks': [{'id': c['id'], 'index': c['index']} for c in chunks],
        'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'checksum': hashlib.md5(file_data).hexdigest()
    }
    
    return jsonify({
        'file_id': file_id,
        'chunks': len(chunks),
        'size': len(file_data)
    })

@app.route('/download/<file_id>')
def download(file_id):
    if file_id not in file_metadata:
        return jsonify({'error': 'File not found'}), 404
    
    metadata = file_metadata[file_id]
    
    # Reassemble chunks
    chunks_data = []
    for chunk_info in sorted(metadata['chunks'], key=lambda x: x['index']):
        chunk_data = load_chunk(chunk_info['id'])
        if chunk_data:
            chunks_data.append(chunk_data)
    
    if len(chunks_data) != len(metadata['chunks']):
        return jsonify({'error': 'Some chunks missing'}), 500
    
    # Combine chunks
    file_data = b''.join(chunks_data)
    
    # Verify integrity
    if hashlib.md5(file_data).hexdigest() != metadata['checksum']:
        return jsonify({'error': 'File integrity check failed'}), 500
    
    # Save temp file and send
    temp_path = f"temp_{file_id}"
    with open(temp_path, 'wb') as f:
        f.write(file_data)
    
    from flask import send_file
    return send_file(temp_path, as_attachment=True, download_name=metadata['filename'])

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'files': len(file_metadata),
        'chunks': len(os.listdir(STORAGE_DIR))
    })

@app.route('/files')
def files():
    return jsonify(file_metadata)

if __name__ == '__main__':
    print("SDFBS Phase 1 - Distributed File System")
    print("Open: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)