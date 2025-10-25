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

### 3️⃣ Setup Instructions

### **Step 1:** Open VS Code Terminal
Press `Ctrl + `` or Terminal → New Terminal

### **Step 2:** Navigate to Directory
```
cd phase1-core-infrastructure
```

### **Step 3:** Install Flask
```
pip install flask
```

### **Step 4:** Choose Mode and Start

**Simple Mode (Development):**
```
python simple_distributed.py
```

**Complete Distributed (Multi-Node):**
```
python complete_distributed.py
```

**With Redundancy (Recommended):**
```
python redundant_distributed.py
```

### **Step 5:** Open Browser
Go to: http://localhost:8080

### **Step 6:** Test Upload
1. Select file
2. Click upload button
3. Watch file chunks distribute across nodes
4. Verify redundancy and fault tolerance



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
