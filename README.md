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

### 3️⃣ Build and Launch Services

```bash
docker-compose -f cloud/docker-compose.yml up -d --build
```

✨ Docker will automatically pull, build, and run your entire SDFBS setup!

---

### 4️⃣ Verify Running Containers

```bash
docker ps
```

Check that all containers are running successfully:
- 🗄️ Cassandra Database Nodes  
- 🔁 Node.js File Services  
- ⚖️ Nginx Load Balancer  
- 📈 Elasticsearch, Fluentd, Kibana Stack  

---

### 5️⃣ Access Your Application

| 🌐 Service | 🔗 URL | 📝 Description |
|-------------|---------|----------------|
| **Load Balancer (HTTP)** | [http://localhost:8080](http://localhost:8080) | Access file backup nodes |
| **Load Balancer (HTTPS)** | [https://localhost:8443](https://localhost:8443) | Secure access (self-signed SSL) |
| **Kibana Dashboard** | [http://localhost:5601](http://localhost:5601) | Monitor logs, performance, and metrics |

---

## ⚡ Quick Command Reference

| 🧩 Action | 💻 Command |
|------------|-------------|
| ▶️ **Start All Services** | `docker-compose -f cloud/docker-compose.yml up -d --build` |
| ⏹️ **Stop All Services** | `docker-compose -f cloud/docker-compose.yml down` |
| 🩺 **Show Running Containers** | `docker ps` |
| 📜 **View Logs** | `docker logs <container-name>` |
| 🔄 **Restart Load Balancer** | `docker restart loadbalancer` |

---

## 🧠 Troubleshooting Guide

| ⚠️ Issue | 🩹 Solution |
|-----------|-------------|
| **Port conflicts** | Modify ports in `cloud/docker-compose.yml`. |
| **Docker startup issues** | Restart Docker Desktop and confirm WSL 2 backend is active. |
| **Logs not visible** | Temporarily comment out the Fluentd container for debugging. |
| **System errors** | Use `docker logs <container>` for detailed insights. |

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
