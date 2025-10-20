#  Welcome to Secure Distributed File Backup System (SDFBS) 

![Data Backup](https://media.giphy.com/media/l0MYGEcHFX1VRvlIk/giphy.gif)

Your ultimate **secure**, **distributed**, and **decentralized** file backup platform — designed to keep your data safe, reliable, and scalable like never before!  

---

##  Why SDFBS Rocks?

| Feature           | Why You'll Love it                    |
|-------------------|---------------------------------------|
|  Security       | End-to-end encryption protecting your precious data |
|  Decentralized  | Multi-node Cassandra setup for ultimate redundancy |
|  Dockerized     | Containers for easy, fast, scalable deployments  |
|  Monitoring     | Powerful EFK stack (Elasticsearch, Fluentd, Kibana) for real-time insights |
|  Load Balancer  | Nginx load balancer ensures seamless and reliable access |

![Cloud Scale](https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif)

---

##  Getting Started — Step by Step Guide 

### 1 Pre-flight Check

Ensure:

-  Windows 10/11 with **WSL 2** installed and activated  
-  Latest **Docker Desktop** with WSL 2 integration enabled  
-  Git installed  
-  Visual Studio Code recommended  

---

### 2 Clone the SDFBS Repository 

git clone https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System.git
cd Secure-Distributed-File-Backup-System

text

![Cloning Repo](https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif)

---

### 3 Build & Launch Your Backup Fortress 

docker-compose -f cloud/docker-compose.yml up -d --build

text

Docker will pull images, build containers, and start all services. Sit back and relax!

![Building Containers](https://media.giphy.com/media/26BRv0ThflsHCqDrG/giphy.gif)

---

### 4 Inspect Your Setup 

docker ps

text

You should see your Cassandra nodes, load balancer, and EFK stack containers all running.

---

### 5 Dive Into Your Services 

| Service URL         | Description                      | Visual Cue                        |
|---------------------|---------------------------------|---------------------------------|
| [Load Balancer](http://localhost:8080)  | Main entry to nodes         | ![HTTP Link](https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif) |
| [Secure Access](https://localhost:8443) | HTTPS access (accept warning) | ![Lock](https://media.giphy.com/media/xUOwGp9HfqV2nLLh7m/giphy.gif)      |
| [Kibana Dashboard](http://localhost:5601) | Logs & metrics visualizer | ![Dashboard](https://media.giphy.com/media/xT0BKmtQGLbumr5RCM/giphy.gif)  |

---

##  Quick Commands Cheat Sheet  

| Action               | Command                                        |  
|----------------------|------------------------------------------------|  
|  Start all services | docker-compose -f cloud/docker-compose.yml up -d --build |  
|  Stop all services  | docker-compose -f cloud/docker-compose.yml down |  
|  See running        | docker ps                                     |  
|  Inspect logs       | docker logs <container-name>                  |  
|  Restart Load Balancer | docker restart loadbalancer                 |  

---

##  Troubleshooting Wizard

- Port conflicts? Adjust ports in cloud/docker-compose.yml  
- Docker issues? Restart Docker Desktop and ensure WSL 2 is active  
- Logging issues? Temporarily comment out Fluentd  
- Use logs extensively for problem diagnosis

---

##  Explore Your Project

- cloud/: Core services and deployment  
- efk/: Elasticsearch, Fluentd, Kibana logging stack  
- load_balancer/: Nginx for HTTPS load balancing

---

##  Get Involved!

Contributions welcome! Open issues or pull requests on GitHub.

---

 Now you're ready to keep your data safe and sound, with SDFBS! 
