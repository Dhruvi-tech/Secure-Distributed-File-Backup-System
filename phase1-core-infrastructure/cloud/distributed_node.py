from flask import Flask, request, jsonify, send_file
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
import hashlib
import io
import os
import time
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
NODE_ID = os.getenv('NODE_ID', 'node1')
CASSANDRA_HOSTS = os.getenv('CASSANDRA_HOSTS', 'cassandra1,cassandra2,cassandra3').split(',')
CHUNK_SIZE = 1024 * 1024  # 1MB chunks
REPLICATION_FACTOR = 3

# Global variables
cluster = None
session = None

def connect_to_cassandra():
    """Connect to Cassandra cluster with retry logic"""
    global cluster, session
    max_retries = 10
    retry_delay = 30
    
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting to connect to Cassandra (attempt {attempt + 1})")
            cluster = Cluster(CASSANDRA_HOSTS)
            session = cluster.connect()
            
            # Create keyspace and tables
            session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS sdfbs 
                WITH REPLICATION = {{
                    'class': 'SimpleStrategy',
                    'replication_factor': {REPLICATION_FACTOR}
                }}
            """)
            
            session.set_keyspace('sdfbs')
            
            # Create tables
            session.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    file_id UUID PRIMARY KEY,
                    filename TEXT,
                    file_size BIGINT,
                    chunk_count INT,
                    upload_time TIMESTAMP,
                    checksum TEXT,
                    node_id TEXT
                )
            """)
            
            session.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    file_id UUID,
                    chunk_index INT,
                    chunk_data BLOB,
                    chunk_size INT,
                    node_id TEXT,
                    PRIMARY KEY (file_id, chunk_index)
                )
            """)
            
            session.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    node_id TEXT PRIMARY KEY,
                    status TEXT,
                    last_heartbeat TIMESTAMP,
                    files_count INT,
                    storage_used BIGINT
                )
            """)
            
            logging.info("Successfully connected to Cassandra")
            return True
            
        except Exception as e:
            logging.error(f"Failed to connect to Cassandra: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Max retries reached. Could not connect to Cassandra.")
                return False
    
    return False

def chunk_file(file_data):
    """Split file into chunks for distributed storage"""
    chunks = []
    for i in range(0, len(file_data), CHUNK_SIZE):
        chunks.append(file_data[i:i + CHUNK_SIZE])
    return chunks

def distribute_chunks(file_id, chunks):
    """Distribute chunks across multiple nodes with redundancy"""
    for i, chunk in enumerate(chunks):
        # Store chunk with replication
        session.execute("""
            INSERT INTO chunks (file_id, chunk_index, chunk_data, chunk_size, node_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (file_id, i, chunk, len(chunk), NODE_ID))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test Cassandra connection
        session.execute("SELECT now() FROM system.local")
        return jsonify({'status': 'healthy', 'node_id': NODE_ID})
    except:
        return jsonify({'status': 'unhealthy', 'node_id': NODE_ID}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload file with distributed storage and redundancy"""
    try:
        file = request.files['file']
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        
        file_data = file.read()
        file_id = uuid.uuid4()
        checksum = hashlib.md5(file_data).hexdigest()
        
        # Chunk the file
        chunks = chunk_file(file_data)
        
        # Store file metadata
        session.execute("""
            INSERT INTO files (file_id, filename, file_size, chunk_count, upload_time, checksum, node_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (file_id, file.filename, len(file_data), len(chunks), datetime.now(), checksum, NODE_ID))
        
        # Distribute chunks
        distribute_chunks(file_id, chunks)
        
        # Update node statistics
        session.execute("""
            UPDATE nodes SET last_heartbeat = %s, files_count = files_count + 1, storage_used = storage_used + %s
            WHERE node_id = %s
        """, (datetime.now(), len(file_data), NODE_ID))
        
        logging.info(f"File {file.filename} uploaded successfully with {len(chunks)} chunks")
        
        return jsonify({
            'file_id': str(file_id),
            'filename': file.filename,
            'chunks': len(chunks),
            'node_id': NODE_ID,
            'status': 'uploaded'
        })
        
    except Exception as e:
        logging.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<file_id>')
def download_file(file_id):
    """Download file by reassembling chunks from distributed storage"""
    try:
        # Get file metadata
        file_info = session.execute("""
            SELECT filename, chunk_count, checksum FROM files WHERE file_id = %s
        """, (uuid.UUID(file_id),)).one()
        
        if not file_info:
            return jsonify({'error': 'File not found'}), 404
        
        # Get all chunks in order
        chunks_result = session.execute("""
            SELECT chunk_data FROM chunks WHERE file_id = %s ORDER BY chunk_index
        """, (uuid.UUID(file_id),))
        
        # Reassemble file
        file_data = b''.join([row.chunk_data for row in chunks_result])
        
        # Verify integrity
        if hashlib.md5(file_data).hexdigest() != file_info.checksum:
            return jsonify({'error': 'File integrity check failed'}), 500
        
        return send_file(
            io.BytesIO(file_data),
            as_attachment=True,
            download_name=file_info.filename
        )
        
    except Exception as e:
        logging.error(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/files')
def list_files():
    """List all files in the distributed system"""
    try:
        files = session.execute("SELECT file_id, filename, file_size, upload_time, node_id FROM files")
        return jsonify([{
            'file_id': str(row.file_id),
            'filename': row.filename,
            'file_size': row.file_size,
            'upload_time': row.upload_time.isoformat(),
            'node_id': row.node_id
        } for row in files])
    except Exception as e:
        logging.error(f"List files error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/nodes')
def list_nodes():
    """List all nodes in the cluster"""
    try:
        nodes = session.execute("SELECT node_id, status, last_heartbeat, files_count, storage_used FROM nodes")
        return jsonify([{
            'node_id': row.node_id,
            'status': row.status,
            'last_heartbeat': row.last_heartbeat.isoformat() if row.last_heartbeat else None,
            'files_count': row.files_count or 0,
            'storage_used': row.storage_used or 0
        } for row in nodes])
    except Exception as e:
        logging.error(f"List nodes error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def node_status():
    """Get current node status"""
    try:
        # Update heartbeat
        session.execute("""
            INSERT INTO nodes (node_id, status, last_heartbeat, files_count, storage_used)
            VALUES (%s, %s, %s, %s, %s)
        """, (NODE_ID, 'active', datetime.now(), 0, 0))
        
        return jsonify({
            'node_id': NODE_ID,
            'status': 'active',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Connect to Cassandra on startup
    if connect_to_cassandra():
        logging.info(f"Starting distributed node {NODE_ID}")
        app.run(host='0.0.0.0', port=8000, debug=False)
    else:
        logging.error("Failed to start node - could not connect to Cassandra")
        exit(1)