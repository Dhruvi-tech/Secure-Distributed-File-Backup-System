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

## 🚀 Quick Start (3 Modes)

### Mode 1: Simple (Single Server)
```cmd
run_simple.bat
```
- Access: http://localhost:8080
- Features: Basic upload/download, local storage

### Mode 2: Standalone (API + Web)
```cmd
run_standalone.bat
```
- API: http://localhost:8080
- Web: http://localhost:3001
- Features: Separate frontend/backend

### Mode 3: Cloud (Distributed)
```cmd
cd cloud
start_cloud.bat
```
- Access: http://localhost:8080 (Load Balanced)
- Features: 3 nodes, Cassandra, chunking, redundancy

## 📁 Phase 1 Files (6 Total)

### Core Server Files
- `simple_server.py` - Single Flask server with built-in web interface
- `standalone_server.py` - API-only server for file operations
- `web_server.py` - Static web server for standalone mode

### Launcher Scripts
- `run_simple.bat` - Starts simple mode (installs Flask + runs simple_server.py)
- `run_standalone.bat` - Starts both API and web servers in separate windows

### Configuration
- `requirements.txt` - Python dependencies (Flask, Flask-CORS, Cassandra driver)

### Cloud Directory (Docker Architecture)
- `cloud/` - Contains distributed system files (7 files for Docker mode)

## Next Phase
Phase 2 will add security features including encryption, authentication, and anomaly detection.