from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from flask_cors import CORS
import uuid
import hashlib
import os
import json
from datetime import datetime
import random
import time

# Import security modules
from phase2_security_enhancements import auth, encryption, models
from utils import chunking_utils, distribution_utils
from utils.logging_utils import secure_logger, error_handler

# Add path for security imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'phase2_security_enhancements'))

app = Flask(__name__)
CORS(app)

# Storage configurations for different modes
STORAGE_CONFIGS = {
    'simple': {
        'dir': 'files_simple',
        'metadata': 'metadata_simple.json'
    },
    'distributed': {
        'dir': 'files_distributed',
        'metadata': 'metadata_distributed.json'
    },
    'production': {
        'dir': 'files_production',
        'metadata': 'metadata_production.json'
    },
    'secure': {
        'dir': 'files_secure',
        'metadata': 'metadata_secure.json'
    }
}

# Create storage directories
for config in STORAGE_CONFIGS.values():
    os.makedirs(config['dir'], exist_ok=True)

# Clear metadata files on server restart to reset file counts
for config in STORAGE_CONFIGS.values():
    metadata_file = config['metadata']
    if os.path.exists(metadata_file):
        os.remove(metadata_file)

# Mock users for secure mode
USERS_FILE = 'users.json'
if not os.path.exists(USERS_FILE):
    default_users = {
        'admin': {
            'password': 'admin123',
            'is_admin': True,
            'created_at': datetime.now().isoformat()
        },
        'user': {
            'password': 'user123',
            'is_admin': False,
            'created_at': datetime.now().isoformat()
        }
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f)

# Mock nodes for distributed mode
NODES_FILE = 'nodes.json'
if not os.path.exists(NODES_FILE):
    mock_nodes = [
        {
            'node_id': 'node-01',
            'status': 'active',
            'files_count': 5,
            'storage_used': 2048000,  # 2MB
            'last_heartbeat': datetime.now().isoformat()
        },
        {
            'node_id': 'node-02',
            'status': 'active',
            'files_count': 3,
            'storage_used': 1536000,  # 1.5MB
            'last_heartbeat': datetime.now().isoformat()
        },
        {
            'node_id': 'node-03',
            'status': 'inactive',
            'files_count': 0,
            'storage_used': 0,
            'last_heartbeat': datetime.now().isoformat()
        }
    ]
    with open(NODES_FILE, 'w') as f:
        json.dump(mock_nodes, f)

def load_metadata(mode):
    config = STORAGE_CONFIGS[mode]
    if os.path.exists(config['metadata']):
        with open(config['metadata'], 'r') as f:
            return json.load(f)
    return {}

def save_metadata(mode, metadata):
    config = STORAGE_CONFIGS[mode]
    with open(config['metadata'], 'w') as f:
        json.dump(metadata, f, default=str)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, default=str)

def load_nodes():
    # Always return fresh nodes on server restart for distributed mode
    return [
        {
            'node_id': 'node-01',
            'status': 'active',
            'files_count': 0,
            'storage_used': 0,
            'last_heartbeat': datetime.now().isoformat()
        },
        {
            'node_id': 'node-02',
            'status': 'active',
            'files_count': 0,
            'storage_used': 0,
            'last_heartbeat': datetime.now().isoformat()
        },
        {
            'node_id': 'node-03',
            'status': 'active',
            'files_count': 0,
            'storage_used': 0,
            'last_heartbeat': datetime.now().isoformat()
        }
    ]

def save_nodes(nodes):
    with open(NODES_FILE, 'w') as f:
        json.dump(nodes, f, default=str)

# Routes
@app.route('/')
def serve_dashboard():
    return send_from_directory('.', 'unified_dashboard.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory('.', 'script.js')

def split_file_into_chunks(file_data, chunk_size=1024*1024):  # 1MB chunks
    """Split file data into chunks for fault tolerance - now using shared utils"""
    return chunking_utils.split_file_into_chunks(file_data)

def distribute_chunks_across_nodes(chunks, nodes, replication_factor=2):
    """Distribute chunks across nodes with redundancy - now using shared utils"""
    return distribution_utils.distribute_chunks_across_nodes(chunks, nodes, 'files_distributed')

def simulate_node_failure():
    """Randomly simulate node failures for fault tolerance testing"""
    nodes = load_nodes()
    # 20% chance of a node failing
    for node in nodes:
        if random.random() < 0.2 and node['status'] == 'active':
            node['status'] = 'failed'
            print(f"🚨 Node {node['node_id']} failed!")
    save_nodes(nodes)
    return nodes

def reconstruct_file_from_chunks(file_id, mode):
    """Reconstruct file from surviving chunks - now using shared utils"""
    metadata = load_metadata(mode)
    if file_id not in metadata or 'chunk_distribution' not in metadata[file_id]:
        return None

    file_info = metadata[file_id]
    chunk_distribution = file_info['chunk_distribution']
    nodes = load_nodes()
    active_nodes = [n for n in nodes if n['status'] == 'active']

    return distribution_utils.reconstruct_from_distribution(file_id, chunk_distribution, active_nodes)

# API Routes for different modes
@app.route('/<mode>/upload', methods=['POST'])
def upload_file(mode):
    if mode not in STORAGE_CONFIGS:
        return jsonify({'error': 'Invalid mode'}), 400

    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    file_data = file.read()
    file_id = str(uuid.uuid4())
    config = STORAGE_CONFIGS[mode]

    # Simulate node failure before processing
    if mode == 'distributed':
        simulate_node_failure()

    if mode == 'distributed':
        # Split file into chunks for fault tolerance
        chunks = split_file_into_chunks(file_data)
        nodes = load_nodes()
        chunk_distribution = distribute_chunks_across_nodes(chunks, nodes)

        # Save metadata with chunk information
        metadata = load_metadata(mode)
        metadata[file_id] = {
            'filename': file.filename,
            'file_size': len(file_data),
            'upload_time': datetime.now().isoformat(),
            'node_id': 'distributed',
            'chunks': chunks,
            'chunk_distribution': chunk_distribution,
            'replication_factor': 2,
            'checksum': hashlib.md5(file_data).hexdigest(),
            'encrypted': mode == 'secure'
        }
        save_metadata(mode, metadata)
        save_nodes(nodes)

        return jsonify({
            'message': 'File uploaded with fault tolerance',
            'file_id': file_id,
            'chunks': len(chunks),
            'replication_factor': 2,
            'distributed_across': len(set([loc['node_id'] for dist in chunk_distribution.values() for loc in dist]))
        })

    else:
        # Simple mode - save as single file
        file_path = os.path.join(config['dir'], file_id)
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Save metadata
        metadata = load_metadata(mode)
        metadata[file_id] = {
            'filename': file.filename,
            'file_size': len(file_data),
            'upload_time': datetime.now().isoformat(),
            'node_id': 'local',
            'chunks': 1,
            'checksum': hashlib.md5(file_data).hexdigest(),
            'encrypted': mode == 'secure'
        }
        save_metadata(mode, metadata)

        return jsonify({
            'message': 'File uploaded successfully',
            'file_id': file_id,
            'node_id': 'local',
            'chunks': 1
        })

@app.route('/<mode>/files')
def get_files(mode):
    if mode not in STORAGE_CONFIGS:
        return jsonify({'error': 'Invalid mode'}), 400

    metadata = load_metadata(mode)
    # Convert to list and add file_id
    files = []
    for file_id, info in metadata.items():
        info_copy = info.copy()
        info_copy['file_id'] = file_id

        # Add fault tolerance status for distributed mode
        if mode == 'distributed' and 'chunk_distribution' in info_copy:
            nodes = load_nodes()
            active_nodes = {n['node_id']: n for n in nodes if n['status'] == 'active'}
            chunk_distribution = info_copy['chunk_distribution']

            available_chunks = 0
            total_chunks = len(chunk_distribution)
            failed_nodes = []

            for chunk_id, locations in chunk_distribution.items():
                chunk_available = False
                for location in locations:
                    if location['node_id'] in active_nodes and os.path.exists(location['path']):
                        chunk_available = True
                        break
                if chunk_available:
                    available_chunks += 1
                else:
                    # Check which nodes failed for this chunk
                    for location in locations:
                        if location['node_id'] not in active_nodes:
                            failed_nodes.append(location['node_id'])

            info_copy['fault_tolerance'] = {
                'available_chunks': available_chunks,
                'total_chunks': total_chunks,
                'reconstructable': available_chunks == total_chunks,
                'failed_nodes': list(set(failed_nodes))
            }

        files.append(info_copy)

    return jsonify(files)

@app.route('/<mode>/nodes')
def get_nodes(mode):
    if mode == 'distributed':
        nodes = load_nodes()
        # Simulate varying heartbeat times and occasional failures
        for node in nodes:
            if random.random() < 0.1:  # 10% chance to update heartbeat
                node['last_heartbeat'] = datetime.now().isoformat()
            # Occassionally recover failed nodes (5% chance)
            if node['status'] == 'failed' and random.random() < 0.05:
                node['status'] = 'active'
                print(f"✅ Node {node['node_id']} recovered!")
        save_nodes(nodes)
        return jsonify(nodes)
    elif mode == 'simple':
        # Simple mode has one local node
        return jsonify([{
            'node_id': 'local',
            'status': 'active',
            'files_count': len(load_metadata('simple')),
            'storage_used': sum(f['file_size'] for f in load_metadata('simple').values()),
            'last_heartbeat': datetime.now().isoformat()
        }])
    elif mode == 'production':
        # Production mode has master-slave setup
        production_metadata = load_metadata('production')
        files_count = len(production_metadata)
        storage_used = sum(f['file_size'] for f in production_metadata.values())
        return jsonify([
            {
                'node_id': 'master',
                'status': 'active',
                'files_count': files_count,
                'storage_used': storage_used,
                'last_heartbeat': datetime.now().isoformat()
            },
            {
                'node_id': 'slave-01',
                'status': 'active',
                'files_count': files_count,
                'storage_used': storage_used,
                'last_heartbeat': datetime.now().isoformat()
            },
            {
                'node_id': 'slave-02',
                'status': 'active',
                'files_count': files_count,
                'storage_used': storage_used,
                'last_heartbeat': datetime.now().isoformat()
            }
        ])
    else:
        return jsonify([])

@app.route('/<mode>/download/<file_id>')
def download_file(mode, file_id):
    if mode not in STORAGE_CONFIGS:
        return jsonify({'error': 'Invalid mode'}), 400

    metadata = load_metadata(mode)
    if file_id not in metadata:
        return jsonify({'error': 'File not found'}), 404

    file_info = metadata[file_id]

    if mode == 'distributed':
        # Reconstruct file from chunks with fault tolerance
        file_data, missing_chunks = reconstruct_file_from_chunks(file_id, mode)

        if file_data is None:
            return jsonify({
                'error': 'File cannot be reconstructed',
                'missing_chunks': missing_chunks,
                'message': 'Some chunks are unavailable due to node failures'
            }), 500

        from io import BytesIO
        file_stream = BytesIO(file_data)
        file_stream.seek(0)

        return send_file(file_stream, as_attachment=True,
                        download_name=file_info['filename'])

    else:
        # Simple mode - direct file access
        config = STORAGE_CONFIGS[mode]
        file_path = os.path.join(config['dir'], file_id)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found on disk'}), 404

        return send_file(file_path, as_attachment=True,
                        download_name=file_info['filename'])

# Secure mode authentication routes
@app.route('/secure/login')
def secure_login_page():
    return render_template('login.html')

@app.route('/secure/dashboard')
def secure_dashboard():
    return render_template('secure_mode.html')

@app.route('/secure/login', methods=['POST'])
def secure_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user_data = auth.auth_manager.authenticate_user(username, password)

        if user_data:
            token = auth.auth_manager.generate_token(user_data)
            secure_logger.log_auth_attempt(username, True, request.remote_addr, request.user_agent.string)

            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'username': user_data['username'],
                    'is_admin': user_data['is_admin']
                }
            })

        secure_logger.log_auth_attempt(username, False, request.remote_addr, request.user_agent.string)
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    except Exception as e:
        secure_logger.log_error("Login error", "authentication", e)
        return jsonify({'success': False, 'error': 'Authentication service unavailable'}), 500

@app.route('/secure/register', methods=['POST'])
def secure_register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin', False)

        user_data = auth.auth_manager.register_user(username, password, is_admin)

        secure_logger.log_security_event("User registration", username,
                                       request.remote_addr, {"is_admin": is_admin})

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'username': user_data['username'],
                'is_admin': user_data['is_admin'],
                'created_at': user_data['created_at']
            }
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        secure_logger.log_error("Registration error", "authentication", e)
        return jsonify({'success': False, 'error': 'Registration service unavailable'}), 500

# Production mode specific endpoints
@app.route('/production/cluster')
def get_cluster_status():
    # Dynamic cluster data based on actual file counts
    production_files = load_metadata('production')
    total_files = len(production_files)
    total_chunks = sum(3 for _ in production_files)  # 3 chunks per file

    return jsonify({
        'master': {
            'node_id': 'master',
            'status': 'active',
            'files': total_files,
            'chunks': total_chunks,
            'last_sync': datetime.now().isoformat()
        },
        'slaves': [
            {
                'node_id': 'slave-01',
                'status': 'active',
                'files': total_files,
                'chunks': total_chunks,
                'last_sync': datetime.now().isoformat()
            },
            {
                'node_id': 'slave-02',
                'status': 'active',
                'files': total_files,
                'chunks': total_chunks,
                'last_sync': datetime.now().isoformat()
            },
            {
                'node_id': 'slave-03',
                'status': 'active',
                'files': total_files,
                'chunks': total_chunks,
                'last_sync': datetime.now().isoformat()
            }
        ]
    })

@app.route('/production/logs')
def get_replication_logs():
    # Dynamic replication logs based on files
    logs = []
    production_files = load_metadata('production')
    actions = ['replicated', 'synced', 'chunked', 'verified']
    nodes = ['master', 'slave-01', 'slave-02', 'slave-03']

    # Generate logs based on actual files
    if production_files:
        for i, (file_id, file_info) in enumerate(list(production_files.items())[-5:]):  # Last 5 files
            timestamp = datetime.fromisoformat(file_info['upload_time'])
            action = random.choice(actions)
            node = random.choice(nodes)

            logs.append({
                'timestamp': timestamp.isoformat(),
                'type': 'replication',
                'message': f'File "{file_info["filename"]}" {action} to {node}'
            })

            # Add chunking logs
            for chunk in range(3):  # 3 chunks per file
                chunk_time = timestamp.replace(second=min(59, timestamp.second + chunk))
                logs.append({
                    'timestamp': chunk_time.isoformat(),
                    'type': 'replication',
                    'message': f'Chunk {chunk+1}/3 of "{file_info["filename"]}" synced to {random.choice(nodes)}'
                })
    else:
        # Default logs when no files
        for i in range(5):
            current_time = datetime.now()
            timestamp = current_time.replace(second=max(0, current_time.second - i*12))  # 12 second intervals
            action = random.choice(actions)
            node = random.choice(nodes)

            logs.append({
                'timestamp': timestamp.isoformat(),
                'type': 'replication',
                'message': f'System {action} check on {node}'
            })

    # Sort by timestamp (newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(logs[:10])  # Return latest 10 logs

@app.route('/<mode>/redistribute')
def redistribute_chunks(mode):
    """Redistribute chunks from failed nodes to active nodes"""
    if mode != 'distributed':
        return jsonify({'error': 'Redistribution only available for distributed mode'}), 400

    metadata = load_metadata(mode)
    nodes = load_nodes()
    active_nodes = [n for n in nodes if n['status'] == 'active']

    if len(active_nodes) < 2:
        return jsonify({'error': 'Need at least 2 active nodes for redistribution'}), 400

    redistributed_count = 0

    for file_id, file_info in metadata.items():
        if 'chunk_distribution' in file_info:
            chunk_distribution = file_info['chunk_distribution']
            needs_redistribution = False

            for chunk_id, locations in chunk_distribution.items():
                surviving_locations = []
                failed_locations = []

                for location in locations:
                    if any(n['node_id'] == location['node_id'] and n['status'] == 'active' for n in nodes):
                        if os.path.exists(location['path']):
                            surviving_locations.append(location)
                        else:
                            failed_locations.append(location)

                # If we have failed locations and enough active nodes, redistribute
                if failed_locations and len(active_nodes) >= 2:
                    needs_redistribution = True
                    # Find a new active node not already holding this chunk
                    current_node_ids = {loc['node_id'] for loc in surviving_locations}
                    available_nodes = [n for n in active_nodes if n['node_id'] not in current_node_ids]

                    if available_nodes:
                        new_node = random.choice(available_nodes)
                        # Reconstruct chunk data from surviving copy
                        chunk_data = None
                        for surviving_loc in surviving_locations:
                            if os.path.exists(surviving_loc['path']):
                                with open(surviving_loc['path'], 'rb') as f:
                                    chunk_data = f.read()
                                break

                        if chunk_data:
                            # Save to new node
                            chunk_file = f"{chunk_id}_{new_node['node_id']}_{uuid.uuid4().hex[:8]}"
                            chunk_path = os.path.join('files_distributed', chunk_file)

                            with open(chunk_path, 'wb') as f:
                                f.write(chunk_data)

                            # Update distribution
                            chunk_distribution[chunk_id].append({
                                'node_id': new_node['node_id'],
                                'chunk_file': chunk_file,
                                'path': chunk_path
                            })

                            redistributed_count += 1
                            print(f"🔄 Redistributed {chunk_id} to {new_node['node_id']}")

    # Save updated metadata and nodes
    save_metadata(mode, metadata)
    save_nodes(nodes)

    return jsonify({
        'message': f'Redistributed {redistributed_count} chunks',
        'timestamp': datetime.now().isoformat()
    })

# Secure mode protected routes
def token_required(f):
    """Decorator to require authentication token"""
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token required'}), 401

        if token.startswith('Bearer '):
            token = token[7:]

        user_data = auth.auth_manager.get_user_from_token(token)
        if not user_data:
            return jsonify({'error': 'Invalid token'}), 401

        # Add user to request context
        request.current_user = user_data
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

def admin_required(f):
    """Decorator to require admin privileges"""
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user') or not request.current_user['is_admin']:
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route('/secure/upload', methods=['POST'])
@token_required
def secure_upload():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file provided'}), 400

        username = request.current_user['username']
        file_data = file.read()
        file_id = str(uuid.uuid4())

        # Generate encryption key
        encryption_key = encryption.encryption_manager.generate_key()
        key_b64 = encryption.encryption_manager.key_from_b64(encryption_key.hex())

        # Split file into chunks
        chunks = chunking_utils.split_file_into_chunks(file_data)

        # Encrypt chunks
        encrypted_chunks = []
        for chunk in chunks:
            encrypted_data = encryption.encryption_manager.encrypt_chunk(chunk['data'], encryption_key)
            encrypted_chunks.append({
                **chunk,
                'data': encrypted_data,
                'size': len(encrypted_data)
            })

        # Distribute encrypted chunks
        nodes = load_nodes()
        chunk_distribution = distribution_utils.distribute_chunks_across_nodes(
            encrypted_chunks, nodes, 'files_secure'
        )

        # Save file metadata
        file_record = models.file_model.create_file_record(
            file_id=file_id,
            filename=file.filename,
            owner=username,
            file_size=len(file_data),
            encryption_key=key_b64,
            chunks_info=[{k: v for k, v in c.items() if k != 'data'} for c in encrypted_chunks],
            checksum=encryption.encryption_manager.calculate_checksum(file_data)
        )

        # Update user stats
        models.user_model.update_user_stats(
            username,
            models.file_model.get_user_files(username).__len__(),
            sum(f['file_size'] for f in models.file_model.get_user_files(username))
        )

        # Log successful upload
        secure_logger.log_file_operation("upload", file.filename, username, len(file_data), True)
        secure_logger.log_encryption_event("encrypt", file.filename, "AES-256", True)

        return jsonify({
            'message': 'File encrypted and uploaded securely',
            'file_id': file_id,
            'chunks': len(chunks),
            'encrypted': True,
            'checksum': file_record['checksum']
        })

    except Exception as e:
        error_response = error_handler.handle_file_operation_error("upload", file.filename, e, username)
        return jsonify(error_response), 500

@app.route('/secure/files')
@token_required
def secure_files():
    try:
        username = request.current_user['username']
        files = models.file_model.get_user_files(username)

        return jsonify(files)

    except Exception as e:
        secure_logger.log_error("Error fetching secure files", "file_operations", e, username)
        return jsonify({'error': 'Unable to fetch files'}), 500

@app.route('/secure/download/<file_id>')
@token_required
def secure_download(file_id):
    try:
        username = request.current_user['username']

        # Get file record
        file_record = models.file_model.get_file_record(file_id)
        if not file_record or file_record['owner'] != username:
            return jsonify({'error': 'File not found or access denied'}), 404

        # Reconstruct encrypted file
        chunk_distribution = {}  # This would need to be stored in metadata
        nodes = load_nodes()
        active_nodes = [n for n in nodes if n['status'] == 'active']

        # For secure mode, we need to store chunk_distribution in file_record
        # This is a simplified version - in production, chunk_distribution should be persisted
        encrypted_data, missing_chunks = distribution_utils.reconstruct_from_distribution(
            file_id, chunk_distribution, active_nodes
        )

        if encrypted_data is None:
            return jsonify({
                'error': 'File cannot be reconstructed',
                'missing_chunks': missing_chunks
            }), 500

        # Decrypt file
        encryption_key = encryption.encryption_manager.key_from_b64(file_record['encryption_key'])
        file_data = encryption.encryption_manager.decrypt_file(encrypted_data, encryption_key)

        # Verify checksum
        if not encryption.encryption_manager.verify_checksum(file_data, file_record['checksum']):
            secure_logger.log_encryption_event("decrypt", file_record['filename'], success=False)
            return jsonify({'error': 'File integrity check failed'}), 500

        # Update download stats
        models.file_model.update_download_stats(file_id)

        # Log successful download
        secure_logger.log_file_operation("download", file_record['filename'], username, len(file_data), True)
        secure_logger.log_encryption_event("decrypt", file_record['filename'], "AES-256", True)

        from io import BytesIO
        file_stream = BytesIO(file_data)
        file_stream.seek(0)

        return send_file(file_stream, as_attachment=True, download_name=file_record['filename'])

    except Exception as e:
        error_response = error_handler.handle_file_operation_error("download", "unknown", e, username)
        return jsonify(error_response), 500

@app.route('/secure/delete/<file_id>', methods=['DELETE'])
@token_required
def secure_delete(file_id):
    try:
        username = request.current_user['username']

        if models.file_model.delete_file_record(file_id, username):
            # Update user stats
            models.user_model.update_user_stats(
                username,
                models.file_model.get_user_files(username).__len__(),
                sum(f['file_size'] for f in models.file_model.get_user_files(username))
            )

            secure_logger.log_file_operation("delete", "unknown", username, success=True)
            return jsonify({'message': 'File deleted successfully'})

        return jsonify({'error': 'File not found or access denied'}), 404

    except Exception as e:
        secure_logger.log_error("Error deleting secure file", "file_operations", e, username)
        return jsonify({'error': 'Unable to delete file'}), 500

@app.route('/secure/stats')
@token_required
def secure_stats():
    try:
        username = request.current_user['username']
        user_files = models.file_model.get_user_files(username)

        total_size = sum(f['file_size'] for f in user_files)
        last_activity = max((f.get('last_download') for f in user_files if f.get('last_download')), default='Never')

        return jsonify({
            'files_count': len(user_files),
            'storage_used_mb': round(total_size / (1024 * 1024), 2),
            'last_activity': last_activity if last_activity != 'Never' else 'No downloads yet'
        })

    except Exception as e:
        secure_logger.log_error("Error fetching secure stats", "statistics", e, username)
        return jsonify({'error': 'Unable to fetch statistics'}), 500

# Health check
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'SDFBS Unified Server is running',
        'modes': list(STORAGE_CONFIGS.keys()),
        'secure_mode': 'enabled',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 SDFBS - Unified Dashboard Server")
    print("📊 Modes: Simple, Distributed, Production, Secure")
    print("🌐 Access: http://localhost:8080")
    print("📱 Dashboard: http://localhost:8080")
    print("")
    print("🎨 Features:")
    print("  ✨ Futuristic UI with glassmorphism")
    print("  🎭 Mode-specific themes and animations")
    print("  🔐 Secure authentication system")
    print("  📊 Real-time statistics and monitoring")
    print("  🎆 Particle effects and smooth transitions")
    print("")
    app.run(host='0.0.0.0', port=8080, debug=True)