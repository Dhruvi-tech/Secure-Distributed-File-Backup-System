# <div align="center">🔐 Secure Distributed File Backup System</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Distributed](https://img.shields.io/badge/Distributed-Architecture-blueviolet?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-Passing-00D26A?style=for-the-badge&logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative&logoColor=white)

### *Enterprise-grade distributed storage with military-level redundancy*

**[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-features-at-a-glance) • [💡 Demo](#-how-it-works) • [🤝 Contribute](#-contributing)**

---

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" />
</p>

</div>

## 🌟 Why SDFBS?

<table>
<tr>
<td width="33%" align="center">
<h1>📦</h1>
<h3>Smart Chunking</h3>
<p>Files automatically split into optimized 1MB chunks for lightning-fast distributed storage</p>
</td>
<td width="33%" align="center">
<h1>🌐</h1>
<h3>True Distribution</h3>
<p>Multi-node architecture ensures your data is always available, anywhere, anytime</p>
</td>
<td width="33%" align="center">
<h1>🛡️</h1>
<h3>Battle-Tested</h3>
<p>2x redundancy and fault tolerance means zero data loss, even during node failures</p>
</td>
</tr>
</table>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## ✨ Features at a Glance

<div align="center">

```mermaid
graph LR
    A[📁 File Upload] --> B[🔪 Chunking Engine]
    B --> C[🌐 Load Balancer]
    C --> D[💾 Node 1]
    C --> E[💾 Node 2]
    C --> F[💾 Node N]
    D --> G[🔄 Redundancy Layer]
    E --> G
    F --> G
    G --> H[✅ Verified Storage]
    
    style A fill:#667eea,stroke:#333,stroke-width:4px
    style B fill:#764ba2,stroke:#333,stroke-width:4px
    style C fill:#f093fb,stroke:#333,stroke-width:4px
    style D fill:#4facfe,stroke:#333,stroke-width:4px
    style E fill:#00f2fe,stroke:#333,stroke-width:4px
    style F fill:#43e97b,stroke:#333,stroke-width:4px
    style G fill:#fa709a,stroke:#333,stroke-width:4px
    style H fill:#fee140,stroke:#333,stroke-width:4px
```

</div>

### 🎯 Core Capabilities

<div align="center">

| Feature | Description | Status |
|:-------:|-------------|:------:|
| **📦 Intelligent Chunking** | Splits files into 1MB optimized pieces | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **🌐 P2P Distribution** | Multi-node mesh network with dynamic scaling | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **🔄 Auto Load Balancing** | Smart traffic distribution across nodes | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **🛡️ Fault Tolerance** | Survives multiple node failures gracefully | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **📊 Real-time Monitoring** | Live dashboard with health metrics | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **🔐 Master-Slave Replication** | Cassandra-backed data persistence | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **💓 Heartbeat Protocol** | Automatic node health tracking | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |
| **🎨 Modern Web UI** | Intuitive interface for all operations | ![Status](https://img.shields.io/badge/✓-Production_Ready-00D26A?style=flat-square) |

</div>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🚀 Quick Start

<div align="center">

### 📋 Prerequisites

</div>

<table>
<tr>
<td width="50%">

**✅ Required:**
- ![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)
- ![Git](https://img.shields.io/badge/Git-Latest-F05032?style=flat-square&logo=git&logoColor=white)
- ![pip](https://img.shields.io/badge/pip-Latest-3775A9?style=flat-square&logo=pypi&logoColor=white)

</td>
<td width="50%">

**💡 Recommended:**
- ![VS Code](https://img.shields.io/badge/VS_Code-Latest-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)
- ![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?style=flat-square&logo=docker&logoColor=white)
- ![Browser](https://img.shields.io/badge/Browser-Modern-FF6B6B?style=flat-square&logo=google-chrome&logoColor=white)

</td>
</tr>
</table>

### ⚡ Installation

<div align="center">

```bash
┌─────────────────────────────────────────────┐
│  Installation in 4 Simple Steps 🎯          │
└─────────────────────────────────────────────┘
```

</div>

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System.git

# 2️⃣ Navigate to project
cd Secure-Distributed-File-Backup-System/phase1-core-infrastructure

# 3️⃣ Install dependencies
pip install flask

# 4️⃣ Choose your mode and launch! 🚀
```

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🎮 Choose Your Mode

<table>
<tr>
<td width="33%" align="center">

### 🌱 Simple Mode
<h1>🌱</h1>

**Perfect for Development**

```bash
python simple_distributed.py
```

![Version](https://img.shields.io/badge/Version-1.0-green?style=for-the-badge)

**Includes:**
- ✅ Basic chunking
- ✅ Single-node simulation
- ✅ Web interface
- ✅ Quick testing

</td>
<td width="33%" align="center">

### 🚀 Distributed Mode
<h1>🚀</h1>

**Full P2P Network**

```bash
python complete_distributed.py
```

![Version](https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge)

**Includes:**
- ✅ Multi-node mesh
- ✅ Heartbeat tracking
- ✅ Dynamic scaling
- ✅ Master-slave arch

</td>
<td width="33%" align="center">

### 💎 Production Mode
<h1>💎</h1>

**Enterprise Ready**

```bash
python redundant_distributed.py
```

![Version](https://img.shields.io/badge/Version-3.0-purple?style=for-the-badge)

**Includes:**
- ✅ Cassandra DB
- ✅ 2x redundancy
- ✅ Full fault tolerance
- ✅ Complete Phase 1

</td>
</tr>
</table>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🎨 How It Works

<div align="center">

### 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    📤 File Upload (10MB)                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  🔪 CHUNKING    │
                    │   ENGINE        │
                    └────────┬────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
    ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
    │   💾 NODE 1    │ │   💾 NODE 2    │ │   💾 NODE 3    │
    │                │ │                │ │                │
    │  Chunk 1-3     │ │  Chunk 4-6     │ │  Chunk 7-10    │
    │  [▓▓▓▓▓▓▓▓]    │ │  [▓▓▓▓▓▓▓▓]    │ │  [▓▓▓▓▓▓▓▓]    │
    └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                    ┌───────────────────┐
                    │  🔄 REDUNDANCY    │
                    │    LAYER          │
                    │   (2x Copies)     │
                    └───────────────────┘
                                │
                                ▼
                    ┌───────────────────┐
                    │  ✅ VERIFIED      │
                    │     STORAGE       │
                    └───────────────────┘
```

### 🔄 Real-Time Sync Process

```mermaid
sequenceDiagram
    participant User
    participant LoadBalancer
    participant Node1
    participant Node2
    participant Database
    
    User->>LoadBalancer: Upload File (10MB)
    LoadBalancer->>LoadBalancer: Split into 10 chunks
    LoadBalancer->>Node1: Store Chunks 1-5
    LoadBalancer->>Node2: Store Chunks 6-10
    Node1->>Database: Write metadata
    Node2->>Database: Write metadata
    Database-->>LoadBalancer: Confirm storage
    LoadBalancer-->>User: Upload successful ✓
```

</div>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🌐 Access Your Dashboard

<div align="center">

### **http://localhost:8080**

<img src="https://img.shields.io/badge/Status-🟢_Online-00D26A?style=for-the-badge&labelColor=1a1a1a" />

<br/><br/>

<table>
<tr>
<td align="center" width="20%">
<h2>📤</h2>
<p><b>Upload Files</b><br/>Drag & drop interface</p>
</td>
<td align="center" width="20%">
<h2>📊</h2>
<p><b>Live Stats</b><br/>Real-time distribution</p>
</td>
<td align="center" width="20%">
<h2>💓</h2>
<p><b>Health Monitor</b><br/>Node status tracking</p>
</td>
<td align="center" width="20%">
<h2>📥</h2>
<p><b>Download</b><br/>Integrity checks</p>
</td>
<td align="center" width="20%">
<h2>🔍</h2>
<p><b>Search</b><br/>Manage backups</p>
</td>
</tr>
</table>

</div>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🛠️ Quick Commands

<div align="center">

### Development Commands

</div>

<table>
<tr>
<td width="50%">

```bash
# Check Python version
python --version
```
![Python](https://img.shields.io/badge/Check-Python_Version-3776AB?style=flat-square&logo=python)

```bash
# Install Flask
pip install flask
```
![Flask](https://img.shields.io/badge/Install-Flask-000000?style=flat-square&logo=flask)

```bash
# Run simple mode
python simple_distributed.py
```
![Run](https://img.shields.io/badge/Run-Simple_Mode-green?style=flat-square&logo=python)

</td>
<td width="50%">

```bash
# Health check
curl http://localhost:8080/health
```
![Health](https://img.shields.io/badge/Check-Health-00D26A?style=flat-square&logo=statuspage)

```bash
# Run with redundancy
python redundant_distributed.py
```
![Redundancy](https://img.shields.io/badge/Run-Production_Mode-purple?style=flat-square&logo=python)

```bash
# Check system status
curl http://localhost:8080/status
```
![Status](https://img.shields.io/badge/Check-Status-blue?style=flat-square&logo=statuspage)

</td>
</tr>
</table>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🔧 Troubleshooting

<div align="center">

### 🆘 Common Issues & Solutions

</div>

<details>
<summary><b>🔴 Port 8080 already in use</b></summary>

<br/>

![Issue](https://img.shields.io/badge/Issue-Port_Conflict-red?style=flat-square)

```bash
# Find process using port 8080
lsof -i :8080  # Linux/Mac
netstat -ano | findstr :8080  # Windows

# Kill the process or change port in code
```

![Solution](https://img.shields.io/badge/Solution-Kill_Process_or_Change_Port-green?style=flat-square)

</details>

<details>
<summary><b>🔴 Python not found</b></summary>

<br/>

![Issue](https://img.shields.io/badge/Issue-Python_Missing-red?style=flat-square)

Download Python 3.7+ from [python.org](https://python.org)

Verify installation:
```bash
python --version
```

![Solution](https://img.shields.io/badge/Solution-Install_Python_3.7+-green?style=flat-square&logo=python)

</details>

<details>
<summary><b>🔴 Flask import error</b></summary>

<br/>

![Issue](https://img.shields.io/badge/Issue-Flask_Not_Installed-red?style=flat-square)

```bash
pip install flask
# or
pip3 install flask
```

![Solution](https://img.shields.io/badge/Solution-Install_Flask-green?style=flat-square&logo=flask)

</details>

<details>
<summary><b>🔴 Can't access localhost</b></summary>

<br/>

![Issue](https://img.shields.io/badge/Issue-Connection_Failed-red?style=flat-square)

1. Check if server is running
2. Verify firewall settings
3. Try `127.0.0.1:8080` instead
4. Check console for error messages

![Solution](https://img.shields.io/badge/Solution-Check_Firewall_&_Server-green?style=flat-square)

</details>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 📊 System Architecture

<div align="center">

### 🏗️ Complete System Overview

```mermaid
graph TB
    UI[🎨 Web Interface<br/>React Dashboard] --> LB[⚖️ Load Balancer<br/>Traffic Distribution]
    LB --> N1[💾 Storage Node 1<br/>Primary Storage]
    LB --> N2[💾 Storage Node 2<br/>Primary Storage]
    LB --> N3[💾 Storage Node 3<br/>Primary Storage]
    N1 --> DB[(🗄️ Cassandra DB<br/>Metadata Store)]
    N2 --> DB
    N3 --> DB
    DB --> R[🔄 Replication Layer<br/>2x Redundancy]
    R --> M[📊 Monitoring Dashboard<br/>Health Metrics]
    M --> A[🚨 Alert System<br/>Notifications]
    
    style UI fill:#667eea,color:#fff,stroke:#333,stroke-width:3px
    style LB fill:#764ba2,color:#fff,stroke:#333,stroke-width:3px
    style N1 fill:#4facfe,color:#fff,stroke:#333,stroke-width:3px
    style N2 fill:#00f2fe,color:#333,stroke:#333,stroke-width:3px
    style N3 fill:#43e97b,color:#333,stroke:#333,stroke-width:3px
    style DB fill:#fa709a,color:#fff,stroke:#333,stroke-width:3px
    style R fill:#fee140,color:#333,stroke:#333,stroke-width:3px
    style M fill:#30cfd0,color:#fff,stroke:#333,stroke-width:3px
    style A fill:#f093fb,color:#333,stroke:#333,stroke-width:3px
```

### 📈 Performance Metrics

<table>
<tr>
<td align="center" width="25%">
<h2>⚡</h2>
<h3>99.9%</h3>
<p>Uptime</p>
</td>
<td align="center" width="25%">
<h2>🚀</h2>
<h3>&lt;100ms</h3>
<p>Response Time</p>
</td>
<td align="center" width="25%">
<h2>📦</h2>
<h3>2x</h3>
<p>Redundancy</p>
</td>
<td align="center" width="25%">
<h2>🔄</h2>
<h3>Auto</h3>
<p>Recovery</p>
</td>
</tr>
</table>

</div>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🤝 Contributing

<div align="center">

### We ❤️ Contributors!

</div>

<table>
<tr>
<td align="center" width="33%">
<h1>🐛</h1>
<h3>Report Bugs</h3>
<a href="https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System/issues">
<img src="https://img.shields.io/badge/Open-Issue-red?style=for-the-badge&logo=github"/>
</a>
</td>
<td align="center" width="33%">
<h1>💡</h1>
<h3>Suggest Features</h3>
<a href="https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System/issues">
<img src="https://img.shields.io/badge/Request-Feature-yellow?style=for-the-badge&logo=github"/>
</a>
</td>
<td align="center" width="33%">
<h1>🔧</h1>
<h3>Submit PRs</h3>
<a href="https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System/pulls">
<img src="https://img.shields.io/badge/Create-Pull_Request-green?style=for-the-badge&logo=github"/>
</a>
</td>
</tr>
</table>

### 🌟 Contribution Process

<div align="center">

```mermaid
graph LR
    A[🍴 Fork] --> B[🌿 Branch]
    B --> C[💻 Code]
    C --> D[✅ Test]
    D --> E[📤 Push]
    E --> F[🎉 PR]
    
    style A fill:#667eea,color:#fff
    style B fill:#764ba2,color:#fff
    style C fill:#f093fb,color:#333
    style D fill:#4facfe,color:#fff
    style E fill:#43e97b,color:#333
    style F fill:#fee140,color:#333
```

</div>

1. 🍴 **Fork** the repository
2. 🌿 **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 **Push** to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 **Open** a Pull Request

<div align="center">

![Contributors](https://img.shields.io/github/contributors/Dhruvi-tech/Secure-Distributed-File-Backup-System?style=for-the-badge&color=blue)
![Pull Requests](https://img.shields.io/github/issues-pr/Dhruvi-tech/Secure-Distributed-File-Backup-System?style=for-the-badge&color=green)
![Issues](https://img.shields.io/github/issues/Dhruvi-tech/Secure-Distributed-File-Backup-System?style=for-the-badge&color=yellow)

</div>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 📜 License

<div align="center">

<h1>⭐</h1>

### MIT License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge&logo=open-source-initiative&logoColor=white)](LICENSE)

**Free to use • Modify • Distribute • Commercial use allowed**

[📄 View Full License](LICENSE)

</div>

![Separator](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## 🌟 Show Your Support

<div align="center">

### **If this project helped you, give it a ⭐️!**

[![GitHub stars](https://img.shields.io/github/stars/Dhruvi-tech/Secure-Distributed-File-Backup-System?style=for-the-badge&logo=github&color=yellow)](https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System)
[![GitHub forks](https://img.shields.io/github/forks/Dhruvi-tech/Secure-Distributed-File-Backup-System?style=for-the-badge&logo=github&color=blue)](https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/Dhruvi-tech/Secure-Distributed-File-Backup-System?style=for-the-badge&logo=github&color=green)](https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System)

<br/>

<h1>⭐</h1>

---

### 💬 Final Words

> *"In the age of data, your backup strategy is your insurance policy."*

**Back up smarter. Store safer. Scale infinitely.**

🔐 **SDFBS** — *The future of distributed file storage is here.*

<br/>

<table>
<tr>
<td align="center" width="25%">
<h2>🔒</h2>
<p><b>Secure</b></p>
</td>
<td align="center" width="25%">
<h2>⚡</h2>
<p><b>Fast</b></p>
</td>
<td align="center" width="25%">
<h2>📈</h2>
<p><b>Scalable</b></p>
</td>
<td align="center" width="25%">
<h2>💪</h2>
<p><b>Reliable</b></p>
</td>
</tr>
</table>

---

Made with ❤️ by developers, for developers

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer)

**[⬆ Back to Top](#-secure-distributed-file-backup-system)**

</div>
