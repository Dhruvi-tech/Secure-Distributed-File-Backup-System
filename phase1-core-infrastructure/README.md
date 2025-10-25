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

### Option 1: Cloud Architecture (Recommended)
```cmd
cd phase1-core-infrastructure\cloud
start_cloud.bat
```
Access: http://localhost:8080 (Load Balanced)
Dashboard: Open `web_dashboard.html` in browser

### Option 2: Simple Mode (Development)
```cmd
cd phase1-core-infrastructure
run_simple.bat
```
Access: http://localhost:8080

### Option 3: Standalone Mode
```cmd
cd phase1-core-infrastructure
run_standalone.bat
```
Access: http://localhost:3001

## 📁 Phase 1 Components

### Cloud Architecture (Primary)
- `cloud/distributed_node.py` - Distributed storage node with Cassandra
- `cloud/docker-compose.yml` - Multi-node cluster orchestration
- `cloud/nginx.conf` - Load balancer with security features
- `cloud/web_dashboard.html` - Distributed system dashboard
- `cloud/start_cloud.bat` - Cloud deployment script

### Development Options
- `simple_server.py` - Single-file server for testing
- `standalone_server.py` - Standalone API server
- `web_server.py` - Web interface server
- `run_simple.bat` - Simple mode launcher
- `run_standalone.bat` - Standalone mode launcher

## Next Phase
Phase 2 will add security features including encryption, authentication, and anomaly detection.