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

### 3️⃣ Step-by-Step Setup

#### Option 1: Simple Mode (Recommended)

**Step 1:** Navigate to Phase 1 directory
```cmd
cd phase1-core-infrastructure
```

**Step 2:** Install Python dependencies
```cmd
pip install flask
```

**Step 3:** Start the server
```cmd
python simple_server.py
```

**Step 4:** Open your browser and go to:
```
http://localhost:8080
```



#### Option 2: Standalone Mode

**Step 1:** Navigate to Phase 1 directory
```cmd
cd phase1-core-infrastructure
```

**Step 2:** Install required packages
```cmd
pip install flask flask-cors
```

**Step 3:** Start API server (in first terminal)
```cmd
python standalone_server.py
```

**Step 4:** Start web server (in second terminal)
```cmd
python web_server.py
```

**Step 5:** Access web interface at:
```
http://localhost:3001
```

---

### 4️⃣ Verify System Status

**Simple Mode:**
1. Open http://localhost:8080 in your browser
2. You should see "SDFBS Phase 1 - File Backup" page
3. Try uploading a test file
4. Verify the file appears in the files list



**Standalone Mode:**
1. Check API server at http://localhost:8080
2. Check web interface at http://localhost:3001
3. Upload a file through the web interface  

---

### 5️⃣ Access Your Application

| 🌐 Service | 🔗 URL | 📝 Description |
|-------------|---------|----------------|
| **Simple Mode** | [http://localhost:8080](http://localhost:8080) | Complete file backup system |
| **Standalone Web** | [http://localhost:3001](http://localhost:3001) | Web interface (standalone mode) |


---

## ⚡ Quick Command Reference

| 🧩 Action | 💻 Command |
|------------|-------------|
| ▶️ **Start Simple Mode** | `cd phase1-core-infrastructure && run_simple.bat` |
| ▶️ **Start Standalone Mode** | `cd phase1-core-infrastructure && run_standalone.bat` |
| 🔍 **Check Python Version** | `python --version` |
| 📦 **Install Dependencies** | `pip install flask flask-cors` |

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
