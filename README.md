# 🔐 Secure Distributed File Backup System (SDFBS)

![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![Cassandra](https://img.shields.io/badge/Apache%20Cassandra-Distributed%20DB-blue?logo=apache-cassandra)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen?logo=github-actions)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)
![Contributors](https://img.shields.io/github/contributors/Dhruvi-tech/Secure-Distributed-File-Backup-System?color=orange)

> **A powerful, secure, and scalable decentralized file backup platform built on Docker and Cassandra.**  
> Simplify enterprise-grade data resilience — with encryption, redundancy, and centralized monitoring in one robust system.

---

## 🚀 Key Features

| ⚙️ Feature | 💡 Why You'll Love It |
|------------|------------------------|
| 🔒 **End-to-End Encryption** | Your data stays encrypted both in transit and at rest. |
| 🌐 **Distributed Architecture** | Cassandra ensures high availability and redundancy across multiple nodes. |
| 🐳 **Dockerized Deployment** | One command brings your entire ecosystem online — simple and consistent. |
| 📊 **Centralized Monitoring (EFK Stack)** | Elasticsearch + Fluentd + Kibana give you real-time system visibility. |
| ⚖️ **Load Balancing (Nginx)** | Seamless traffic distribution and fault-tolerant service availability. |

---

## 🧰 Getting Started

### 1️⃣ Prerequisites

Before you begin, ensure you have:

- 💻 **Windows 10/11** with **WSL 2** enabled  
- 🐳 **[Docker Desktop](https://www.docker.com/products/docker-desktop)** (with WSL integration)  
- 🔧 **Git** installed  
- 🧑‍💻 **VS Code** (recommended for editing & development)

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System.git
cd Secure-Distributed-File-Backup-System
```

---

### 3️⃣ Complete Step-by-Step Setup

## 🐳 **Option 1: Docker Mode (Full Distributed System)**

### **Step 1:** Install Docker Desktop
1. Download from https://www.docker.com/products/docker-desktop
2. Install and restart computer
3. Open Docker Desktop, wait for green whale icon
4. Enable WSL 2 in Docker settings

### **Step 2:** Verify Docker
```cmd
docker --version
docker-compose --version
```

### **Step 3:** Navigate to Cloud Directory
```cmd
cd phase1-core-infrastructure\cloud
```

### **Step 4:** Start Services
```cmd
.\start_cloud.bat
```

### **Step 5:** Wait 2-3 Minutes for Cassandra

### **Step 6:** Verify Services
```cmd
docker-compose ps
```

### **Step 7:** Test Health
```cmd
curl http://localhost:8080/health
```

### **Step 8:** Access System
- Load Balancer: http://localhost:8080
- Dashboard: Open `web_dashboard.html`

---

## 🐍 **Option 2: Simple Mode (No Docker)**

### **Step 1:** Check Python
```cmd
python --version
```

### **Step 2:** Navigate to Directory
```cmd
cd phase1-core-infrastructure
```

### **Step 3:** Install Flask
```cmd
pip install flask
```

### **Step 4:** Start Server
```cmd
python simple_server.py
```

### **Step 5:** Open Browser
Go to: http://localhost:8080

### **Step 6:** Test Upload
1. Select file
2. Click Upload
3. Verify in files list

---

## 🔄 **Option 3: Standalone Mode**

### **Step 1:** Install Dependencies
```cmd
cd phase1-core-infrastructure
pip install flask flask-cors
```

### **Step 2:** Start API Server (Terminal 1)
```cmd
python standalone_server.py
```

### **Step 3:** Start Web Server (Terminal 2)
```cmd
python web_server.py
```

### **Step 4:** Access Interface
Go to: http://localhost:3001



---

### 4️⃣ System Verification & Testing

**Docker Mode Verification:**
1. All 7 containers should be running
2. Health endpoint returns "healthy"
3. Web dashboard shows 3 active nodes
4. File upload distributes chunks across nodes

**Simple Mode Verification:**
1. Server starts without errors
2. Web interface loads at localhost:8080
3. File upload and download works
4. Files appear in local storage

**Standalone Mode Verification:**
1. Both servers start successfully
2. API responds at localhost:8080
3. Web interface works at localhost:3001
4. File operations work across both services  

---

### 5️⃣ Access Your Application

| 🌐 Service | 🔗 URL | 📝 Description |
|-------------|---------|----------------|
| **Docker Load Balancer** | [http://localhost:8080](http://localhost:8080) | Distributed system entry point |
| **Docker Dashboard** | `web_dashboard.html` | Open file in browser |
| **Docker Node 1** | [http://localhost:8001](http://localhost:8001) | Direct access to storage node 1 |
| **Docker Node 2** | [http://localhost:8002](http://localhost:8002) | Direct access to storage node 2 |
| **Docker Node 3** | [http://localhost:8003](http://localhost:8003) | Direct access to storage node 3 |
| **Simple Mode** | [http://localhost:8080](http://localhost:8080) | Single server file backup |
| **Standalone API** | [http://localhost:8080](http://localhost:8080) | API server |
| **Standalone Web** | [http://localhost:3001](http://localhost:3001) | Web interface |


---

## ⚡ Quick Command Reference

| 🧩 Action | 💻 Command |
|------------|-------------|
| ▶️ **Start Docker Mode** | `cd phase1-core-infrastructure\cloud && .\start_cloud.bat` |
| ▶️ **Start Simple Mode** | `cd phase1-core-infrastructure && python simple_server.py` |
| ▶️ **Start Standalone Mode** | `cd phase1-core-infrastructure && run_standalone.bat` |
| 🔍 **Check Docker** | `docker --version && docker-compose --version` |
| 🔍 **Check Python** | `python --version` |
| 📦 **Install Flask** | `pip install flask` |
| 📦 **Install All Dependencies** | `pip install flask flask-cors` |
| 🐳 **Stop Docker Services** | `docker-compose down` |
| 🔍 **Check Docker Status** | `docker-compose ps` |

---

## 🧠 Troubleshooting Guide

| ⚠️ Issue | 🩹 Solution |
|-----------|-------------|
| **Port 8080 in use** | Close other applications using port 8080 or change port in code. |
| **Python not found** | Install Python 3.7+ from python.org |
| **Flask not installed** | Run `pip install flask flask-cors` |
| **Can't access localhost** | Check if server is running and firewall allows connections. |

---

## 🤝 Contributing & Support

We welcome all contributions!  
Whether it’s fixing a bug 🐞, improving documentation 📘, or adding a new feature 🚀 — your help matters!

- 💬 **Open an Issue:** [Report a Bug or Request Feature](https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System/issues)
- 🌱 **Submit a PR:** Fork the repo, create your branch, and make a pull request.

---

## 🧾 License

This project is licensed under the **MIT License** — free to use, modify, and distribute with attribution.

📄 [View License](LICENSE)

---

## 💬 Final Words

> 🔐 *Back up smarter, faster, and safer with SDFBS — the future of secure distributed file storage.*  
> Start protecting your data today with confidence and scalability.

---

⭐ **If you like this project, don’t forget to give it a star on GitHub!**
