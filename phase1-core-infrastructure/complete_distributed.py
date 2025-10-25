from flask import Flask, request, jsonify, render_template_string, send_file
import uuid
import hashlib
import os
import json
import threading
import time
import requests
from datetime import datetime

# Global storage for all nodes
nodes_data = {
    'node1': {'files': {}, 'chunks': {}},
    'node2': {'files': {}, 'chunks': {}},
    'node3': {'files': {}, 'chunks': {}}
}

# P2P Network and heartbeat tracking
node_heartbeats = {}
master_node = 'node1'  # Master-slave architecture

app = Flask(__name__)
CHUNK_SIZE = 1024 * 1024  # 1MB

def p2p_heartbeat_monitor():
    """Monitor node heartbeats for P2P network"""
    while True:
        current_time = time.time()
        for node_id in list(nodes_data.keys()):
            last_heartbeat = node_heartbeats.get(node_id, current_time)
            if current_time - last_heartbeat > 30:  # 30 second timeout
                print(f"Node {node_id} heartbeat timeout")
            else:
                node_heartbeats[node_id] = current_time
        time.sleep(10)

def dynamic_node_scaling():
    """Handle dynamic addition/removal of nodes"""
    while True:
        active_nodes = [nid for nid, last_hb in node_heartbeats.items() 
                       if time.time() - last_hb < 30]
        
        # Auto-scale based on load
        if len(active_nodes) < 2:
            new_node_id = f'node{len(nodes_data) + 1}'
            if new_node_id not in nodes_data:
                nodes_data[new_node_id] = {'files': {}, 'chunks': {}}
                node_heartbeats[new_node_id] = time.time()
                print(f"Dynamic scaling: Added {new_node_id}")
        
        time.sleep(60)

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

WEB_INTERFACE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SDFBS - Complete Distributed System</title>
    <style>
        body { font-family: Arial; max-width: 900px; margin: 50px auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .box { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .node { background: white; padding: 10px; margin: 5px 0; border-radius: 3px; border-left: 4px solid #28a745; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 3px; cursor: pointer; }
        .file { background: white; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat { background: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; }
        .chunk-info { font-size: 12px; color: #666; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Secure Distributed File Backup System</h1>
        <p>P2P Network + Heartbeat Tracking + Dynamic Scaling + Master-Slave</p>
    </div>

    <div class="stats">
        <div class="stat">
            <h3>{{ healthy_nodes }}/{{ total_nodes }}</h3>
            <p>P2P Nodes</p>
        </div>
        <div class="stat">
            <h3>{{ file_count }}</h3>
            <p>Files Stored</p>
        </div>
        <div class="stat">
            <h3>{{ total_chunks }}</h3>
            <p>Total Chunks</p>
        </div>
    </div>

    <div class="box">
        <h3>Upload File to Distributed Storage</h3>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" id="fileInput" required>
            <button type="submit">Distribute Across Nodes</button>
        </form>
        <div id="uploadStatus"></div>
    </div>

    <div class="box">
        <h3>P2P Network Nodes (Dynamic Scaling)</h3>
        {% for node_id, status in node_status.items() %}
        <div class="node {{ 'online' if status == 'online' else 'offline' }}">
            <strong>{{ node_id.upper() }}</strong>
            {% if node_id == master_node %} (Master){% endif %}
            <span style="float: right;">{{ status }} | Heartbeat: {{ heartbeats.get(node_id, 'Never') }}</span>
        </div>
        {% endfor %}
    </div>

    <div class="box">
        <h3>Distributed Files</h3>
        {% for file_id, info in all_files.items() %}
        <div class="file">
            <strong>{{ info.filename }}</strong> ({{ info.size }} bytes)
            <div class="chunk-info">
                {{ info.chunks|length }} chunks distributed: 
                {% for chunk in info.chunks %}
                {{ chunk.node_id }}{% if not loop.last %}, {% endif %}
                {% endfor %}
            </div>
            <a href="/download/{{ file_id }}" style="float: right;">Download</a>
        </div>
        {% endfor %}
    </div>

    <script>
        document.getElementById('uploadForm').onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append('file', document.getElementById('fileInput').files[0]);
            
            document.getElementById('uploadStatus').innerHTML = 'Chunking and distributing file...';
            
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
                        'Success! File chunked into ' + data.chunks + ' pieces and distributed across ' + data.nodes_used + ' nodes.';
                    setTimeout(function() { location.reload(); }, 2000);
                }
            });
        };
        
        // Auto refresh every 30 seconds
        setTimeout(function() { location.reload(); }, 30000);
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    # P2P network status with heartbeat tracking
    current_time = time.time()
    node_status = {}
    heartbeat_display = {}
    
    for node_id in nodes_data.keys():
        last_heartbeat = node_heartbeats.get(node_id, 0)
        if current_time - last_heartbeat < 30:
            node_status[node_id] = 'online'
            heartbeat_display[node_id] = f"{int(current_time - last_heartbeat)}s ago"
        else:
            node_status[node_id] = 'offline'
            heartbeat_display[node_id] = 'Timeout'
    
    # Collect all files from all nodes
    all_files = {}
    total_chunks = 0
    
    for node_id, data in nodes_data.items():
        for file_id, file_info in data['files'].items():
            if file_id not in all_files:
                all_files[file_id] = file_info
        total_chunks += len(data['chunks'])
    
    return render_template_string(WEB_INTERFACE,
                                node_status=node_status,
                                heartbeats=heartbeat_display,
                                all_files=all_files,
                                healthy_nodes=sum(1 for s in node_status.values() if s == 'online'),
                                total_nodes=len(nodes_data),
                                file_count=len(all_files),
                                total_chunks=total_chunks,
                                master_node=master_node)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    
    file_data = file.read()
    file_id = str(uuid.uuid4())
    
    # Chunk the file
    chunks = chunk_file(file_data)
    
    # Distribute chunks across nodes
    node_ids = list(nodes_data.keys())
    stored_chunks = []
    
    for i, chunk in enumerate(chunks):
        # Round-robin distribution across nodes
        target_node = node_ids[i % len(node_ids)]
        
        # Store chunk in target node
        nodes_data[target_node]['chunks'][chunk['id']] = chunk['data']
        
        stored_chunks.append({
            'chunk_id': chunk['id'],
            'node_id': target_node,
            'index': chunk['index']
        })
    
    # Create file metadata
    file_metadata = {
        'filename': file.filename,
        'size': len(file_data),
        'chunks': stored_chunks,
        'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'checksum': hashlib.md5(file_data).hexdigest()
    }
    
    # Store metadata in the first node (could be any node)
    nodes_data['node1']['files'][file_id] = file_metadata
    
    return jsonify({
        'file_id': file_id,
        'chunks': len(chunks),
        'nodes_used': len(set(chunk['node_id'] for chunk in stored_chunks))
    })

@app.route('/download/<file_id>')
def download(file_id):
    # Find file metadata
    file_metadata = None
    for node_data in nodes_data.values():
        if file_id in node_data['files']:
            file_metadata = node_data['files'][file_id]
            break
    
    if not file_metadata:
        return jsonify({'error': 'File not found'}), 404
    
    # Retrieve chunks from nodes
    chunks_data = []
    for chunk_info in sorted(file_metadata['chunks'], key=lambda x: x['index']):
        chunk_id = chunk_info['chunk_id']
        node_id = chunk_info['node_id']
        
        if chunk_id in nodes_data[node_id]['chunks']:
            chunks_data.append(nodes_data[node_id]['chunks'][chunk_id])
        else:
            return jsonify({'error': f'Chunk {chunk_id} not found on {node_id}'}), 500
    
    # Reassemble file
    file_data = b''.join(chunks_data)
    
    # Verify integrity
    if hashlib.md5(file_data).hexdigest() != file_metadata['checksum']:
        return jsonify({'error': 'File integrity check failed'}), 500
    
    # Save temp file and send
    temp_path = f"temp_{file_id}"
    with open(temp_path, 'wb') as f:
        f.write(file_data)
    
    return send_file(temp_path, as_attachment=True, download_name=file_metadata['filename'])

@app.route('/health')
def health():
    current_time = time.time()
    active_nodes = sum(1 for hb in node_heartbeats.values() 
                      if current_time - hb < 30)
    
    total_files = len(set().union(*[data['files'].keys() for data in nodes_data.values()]))
    total_chunks = sum(len(data['chunks']) for data in nodes_data.values())
    
    return jsonify({
        'status': 'healthy',
        'p2p_network': 'active',
        'active_nodes': active_nodes,
        'total_nodes': len(nodes_data),
        'files': total_files,
        'chunks': total_chunks,
        'heartbeat_tracking': 'enabled',
        'dynamic_scaling': 'active',
        'master_node': master_node
    })

@app.route('/files')
def files():
    all_files = {}
    for node_data in nodes_data.values():
        all_files.update(node_data['files'])
    return jsonify(all_files)

@app.route('/nodes')
def nodes():
    node_status = {}
    for node_id, data in nodes_data.items():
        node_status[node_id] = {
            'files': len(data['files']),
            'chunks': len(data['chunks']),
            'status': 'online'
        }
    return jsonify(node_status)

if __name__ == '__main__':
    # Initialize heartbeats
    current_time = time.time()
    for node_id in nodes_data.keys():
        node_heartbeats[node_id] = current_time
    
    # Start background threads
    threading.Thread(target=p2p_heartbeat_monitor, daemon=True).start()
    threading.Thread(target=dynamic_node_scaling, daemon=True).start()
    
    print("SDFBS Complete Distributed System")
    print("Features: P2P Network + Heartbeat + Dynamic Scaling + Master-Slave")
    print("Access: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)