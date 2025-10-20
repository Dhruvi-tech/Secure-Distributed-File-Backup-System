#  Secure Distributed File Backup System (SDFBS)

A  **powerful**,  **secure**, and  **scalable** decentralized file backup platform built on Docker and Cassandra.

---

##  Key Features

|  Feature         |  Why You'll Love It                     |
|---------------------|---------------------------------------|
|  End-to-End Encryption | Protects your data at all times    |
|  Distributed Architecture | Redundancy with Cassandra nodes   |
|  Dockerized Deployment | Fast, repeatable container setup   |
|  Centralized Monitoring | EFK stack for logs & performance   |
|  Load Balancing    | Nginx for fault tolerant access      |

---

##  Getting Started

### 1 Prerequisites

- Windows 10/11 with **WSL 2** enabled  
- Latest **[Docker Desktop](https://www.docker.com/products/docker-desktop)** with WSL integration  
- Git installed  
- VS Code for development (recommended)

---

### 2 Clone the repository

git clone https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System.git
cd Secure-Distributed-File-Backup-System

text

---

### 3 Build and Launch Services  

docker-compose -f cloud/docker-compose.yml up -d --build

text

*Docker automagically pulls, builds, and runs your entire backup system!*

---

### 4 Verify Running Containers

docker ps

text

Check that all critical containers are running:
- Cassandra & Node services
- Load balancer
- Elasticsearch, Fluentd, Kibana logging stack

---

### 5 Access Your Application

|  Service            |  URL                   |  Description               |
|-----------------------|--------------------------|-----------------------------|
| Load Balancer (HTTP)  | [http://localhost:8080](http://localhost:8080)   | Access file nodes           |
| Load Balancer (HTTPS) | [https://localhost:8443](https://localhost:8443) | Secure access (self-signed) |
| Kibana Dashboard      | [http://localhost:5601](http://localhost:5601)   | Monitor logs and metrics    |

---

##  Quick Command Reference

|  Action             |  Command                                      |
|-----------------------|------------------------------------------------|
| Start All Services    | docker-compose -f cloud/docker-compose.yml up -d --build |
| Stop All Services     | docker-compose -f cloud/docker-compose.yml down |
| Show Running Containers | docker ps                                   |
| View Container Logs   | docker logs <container-name>                  |
| Restart Load Balancer | docker restart loadbalancer                    |

---

##  Troubleshooting Tips

- **Port conflicts?** Adjust ports in cloud/docker-compose.yml.
- **Docker issues?** Restart Docker Desktop, verify WSL 2 backend.
- **Logging problems?** Temporarily comment out Fluentd container.
- **Always check logs:** Use docker logs <container> for insight.

---

##  Folder Structure Overview

- cloud/: Core services, node apps, Dockerfiles  
- efk/: Elasticsearch, Fluentd, Kibana config  
- load_balancer/: Nginx configs and certificates  

---

##  Contributing & Support

Contributions are welcome! Open GitHub issues or pull requests anytime. Full guidelines coming soon.

---

 Get ready to securely backup your data with confidence using SDFBS! 
