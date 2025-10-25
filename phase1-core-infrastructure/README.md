# Phase 1: Core Infrastructure 🏗️

## Overview
This phase establishes the foundational distributed system architecture with basic file storage and retrieval capabilities.

## Goals
- ✅ Set up Apache Cassandra distributed database
- ✅ Implement basic file chunking and storage
- ✅ Create REST API endpoints for file operations
- ✅ Establish Docker containerization
- ✅ Basic load balancing with Nginx

## Components

### 🗄️ Database Layer
- **Apache Cassandra**: Distributed NoSQL database for storing file chunks
- **Schema Design**: Tables for files, chunks, and metadata
- **Replication**: Basic data redundancy across nodes

### 🔧 Backend Services
- **Node.js/Python Services**: Core file processing logic
- **File Chunking**: Break files into manageable pieces
- **Basic Storage**: Store and retrieve file chunks
- **REST APIs**: HTTP endpoints for file operations

### 🐳 Infrastructure
- **Docker Containers**: Containerized services
- **Docker Compose**: Multi-service orchestration
- **Nginx Load Balancer**: Traffic distribution

## Key Features Delivered
- Basic file upload/download
- File chunking and reassembly
- Distributed storage across Cassandra nodes
- Load-balanced API access
- Container-based deployment

## Success Criteria
- [x] Files can be uploaded and downloaded successfully
- [x] Data is distributed across multiple Cassandra nodes
- [x] System handles basic load balancing
- [x] All services run in Docker containers
- [x] Basic fault tolerance (single node failure)

## 🚀 Quick Start

### Option 1: Simple Mode (Recommended)
```cmd
cd phase1-core-infrastructure
run_simple.bat
```
Then open: http://localhost:8080

### Option 2: Docker Mode
```bash
# Start Docker Desktop first
./start.sh

# Or manually:
docker-compose up -d --build
```

### Option 3: Standalone Mode
```cmd
run_standalone.bat
```
Access: http://localhost:3001

## 📁 Phase 1 Components

### Core Files
- `simple_server.py` - Single-file server with web interface
- `file_service.py` - Distributed file service
- `standalone_server.py` - Standalone API server
- `web_server.py` - Web interface server

### Docker Setup
- `docker-compose.yml` - Multi-service orchestration
- `Dockerfile` - Container configuration
- `cassandra/schema.cql` - Database schema
- `nginx/nginx.conf` - Load balancer configuration

### Scripts
- `run_simple.bat` - Simple mode launcher
- `run_standalone.bat` - Standalone mode launcher
- `start.bat` - Docker mode launcher
- `test_system.py` - Automated testing

## Next Phase
Phase 2 will add security features including encryption, authentication, and anomaly detection.