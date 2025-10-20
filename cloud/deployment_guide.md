# Deployment Guide for Secure Distributed File Backup System (SDFBS)

## Overview
This guide walks through the steps to deploy the SDFBS system infrastructure on your cloud provider using Docker containers and Apache Cassandra.

## Prerequisites
- Cloud VM instances or managed Kubernetes cluster
- Docker and Docker Compose installed on the machines
- Cassandra running locally or on cloud instances
- Network setup with appropriate open ports and security groups

## Steps

### 1. Clone the Repository
\\\ash
git clone https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System.git
cd Secure-Distributed-File-Backup-System
\\\

### 2. Set Up Cassandra Cluster
- Run Cassandra on the cloud VM or use a managed Cassandra service.
- Apply schema using Prisma script:
\\\ash
cd cloud/cassandra_config
./cluster_setup.ps1  # or run schema.cql manually with cqlsh
\\\

### 3. Build and Run Docker Containers
- Navigate to the cloud directory and start your containers:
\\\ash
cd cloud
docker-compose up --build -d
\\\

### 4. Verify Service Status
- Ensure that Cassandra and node containers are running:
\\\ash
docker ps
\\\

### 5. Configure Network and Security
- Set firewall rules to allow access on ports 9042 (Cassandra) and 8000+ (nodes).
- Use TLS certificates for secure communication.

### 6. Scaling
- Add more nodes by updating \docker-compose.yml\ with new services.
- Adjust Cassandra replication settings if required.

### 7. Monitoring and Alerts
- Integrate with cloud monitoring services (CloudWatch, Azure Monitor).
- Deploy anomaly detection scripts on nodes to monitor activity and raise alerts.

---

For detailed system architecture, see \rchitecture/architecture_design.md\.
