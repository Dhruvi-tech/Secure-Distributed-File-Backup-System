from flask import Flask, request, jsonify, send_file, render_template_string
import uuid
import hashlib
import os
import json
from datetime import datetime

app = Flask(__name__)

STORAGE_DIR = "files"
METADATA_FILE = "metadata.json"
os.makedirs(STORAGE_DIR, exist_ok=True)

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, default=str)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SDFBS Phase 1</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .box { background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 3px; cursor: pointer; }
        .file { background: white; padding: 10px; margin: 5px 0; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>SDFBS Phase 1 - File Backup</h1>
    
    <div class="box">
        <h3>Upload File</h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
    </div>

    <div class="box">
        <h3>Files</h3>
        <div id="files">
            {% for file_id, info in files.items() %}
            <div class="file">
                <strong>{{ info.filename }}</strong> ({{ info.file_size }} bytes)
                <a href="/download/{{ file_id }}" style="float: right;">Download</a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    metadata = load_metadata()
    return render_template_string(HTML_TEMPLATE, files=metadata)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "No file selected", 400
    
    file_data = file.read()
    file_id = str(uuid.uuid4())
    
    # Save file
    with open(os.path.join(STORAGE_DIR, file_id), 'wb') as f:
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
    
    return f'<h2>✅ File uploaded successfully!</h2><a href="/">← Back</a>'

@app.route('/download/<file_id>')
def download_file(file_id):
    metadata = load_metadata()
    if file_id not in metadata:
        return "File not found", 404
    
    file_path = os.path.join(STORAGE_DIR, file_id)
    return send_file(file_path, as_attachment=True, 
                    download_name=metadata[file_id]['filename'])

@app.route('/api/files')
def api_files():
    return jsonify(load_metadata())

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "SDFBS Simple Server is running"})

if __name__ == '__main__':
    print("SDFBS Phase 1 - Simple Server")
    print("Open: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)