# 🔐 Secure Distributed File Backup System (SDFBS)

![Python](https://img.shields.io/badge/Python-Flask-blue?logo=python)
![Distributed](https://img.shields.io/badge/Architecture-Distributed-blue)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen?logo=github-actions)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)

> **A powerful, secure, and scalable distributed file backup platform with chunking and redundancy.**  
> Simplify data resilience with file chunking, distributed storage, and fault tolerance in one system.

---

## 🚀 Key Features

| ⚙️ Feature | 💡 Why You'll Love It |
|------------|------------------------|
| 📦 **File Chunking** | Files split into 1MB pieces for distributed storage. |
| 🌐 **Distributed Architecture** | Multi-node storage ensures high availability and redundancy. |
| 🔄 **Load Balancing** | Automatic traffic distribution across storage nodes. |
| 🛡️ **Fault Tolerance** | System survives node failures with redundant storage. |
| 📊 **Real-time Monitoring** | Web dashboard shows system health and node status. |

---

## 🚀 How to Run SDFBS

### Prerequisites:
- 🐍 **Python 3.7+** installed
- 🔧 **Git** installed
- 🧑💻 **VS Code** (recommended)

### Setup:
1. **Clone the repository:**
```bash
git clone https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System.git
cd Secure-Distributed-File-Backup-System
```

2. **Navigate to the project:**
```
cd phase1-core-infrastructure
```

3. **Install Flask:**
```
pip install flask
```

### Choose and Run a Mode:

**🐍 Simple Mode (Development):**
```
python simple_distributed.py
```
*Features: Basic file chunking, single-node simulation, web interface*

**🌐 Complete Distributed (Multi-Node):**
```
python complete_distributed.py
```
*Features: P2P network, heartbeat tracking, dynamic scaling, master-slave architecture*

**🛡️ With Redundancy (Recommended):**
```
python redundant_distributed.py
```
*Features: Cassandra database, master-slave replication, 2x redundancy, complete Phase 1 implementation*

### Access the System:
- Open browser to: **http://localhost:8080**
- Upload files and watch them distribute across nodes
- Monitor system health and redundancy

### Quick Commands:
- Check Python: `python --version`
- Check health: `curl http://localhost:8080/health`

**That's it! The distributed file backup system will be running with web interface, file chunking, and distributed storage.**

---

### 4️⃣ System Verification

1. Server starts without errors
2. Web interface loads at localhost:8080
3. File upload creates chunks distributed across nodes
4. Download reassembles chunks correctly
5. System shows redundancy and fault tolerance
6. Health endpoint returns system status  

---

### 5️⃣ Access Your Application

**Main Interface:** [http://localhost:8080](http://localhost:8080)

- Upload files with automatic chunking
- View distributed storage across nodes
- Monitor system health and redundancy
- Download files with integrity verification

---

## ⚡ Quick Command Reference

| 🧩 Action | 💻 Command |
|------------|-------------|
| ▶️ **Simple Mode** | `python simple_distributed.py` |
| ▶️ **Complete Distributed** | `python complete_distributed.py` |
| ▶️ **With Redundancy** | `python redundant_distributed.py` |
| 🔍 **Check Python** | `python --version` |
| 📦 **Install Flask** | `pip install flask` |
| 🔍 **Check Health** | `curl http://localhost:8080/health` |

---

## 🧠 Troubleshooting Guide

| ⚠️ Issue | 🩹 Solution |
|-----------|-------------|
| **Port 8080 in use** | Close other applications using port 8080 or change port in code. |
| **Python not found** | Install Python 3.7+ from python.org |
| **Flask not installed** | Run `pip install flask` |
| **Can't access localhost** | Check if server is running and firewall allows connections. |

---

## 🤝 Contributing & Support

We welcome all contributions!  
Whether it's fixing a bug 🐞, improving documentation 📘, or adding a new feature 🚀 — your help matters!

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

⭐ **If you like this project, don't forget to give it a star on GitHub!**