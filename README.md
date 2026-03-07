# 🎓 UniEvent: Scalable University Event Portal
**AWS Cloud Architecture & Data Integration Assignment**

## 🌐 Live Deployment
**Application Load Balancer DNS:** (http://unievent-alb-1626878643.us-east-2.elb.amazonaws.com/)

---

## 🏗️ Architecture Overview
This project demonstrates a decoupled, high-availability 3-tier cloud architecture using **Amazon Web Services (AWS)**. The system automates the lifecycle of event data from ingestion to public delivery.



### Key Components:
* **Data Tier:** A Python-based ingestion engine (`fetch_events.py`) that fetches real-time "University" events from the **Ticketmaster Discovery API**.
* **Storage Tier:** **Amazon S3** (`unievent-storage-ahmed-2026`) acts as a stateless data lake, storing event data as JSON objects.
* **App Tier:** A **Flask (Python)** web application hosted on **Amazon EC2** that dynamically renders the S3 data.
* **Networking Tier:** An **Application Load Balancer (ALB)** distributed across multiple Availability Zones to ensure fault tolerance.

---

## 🛠️ Step-by-Step Deployment Guide

Follow these steps to replicate the environment from scratch:

### 1. Network Foundation (VPC)
1.  Create a **VPC** (e.g., `10.0.0.0/16`).
2.  Create two **Public Subnets** in different Availability Zones (e.g., `us-east-1a` and `us-east-1b`).
3.  Attach an **Internet Gateway** and update the Route Table to allow `0.0.0.0/0` traffic.

### 2. Security & Identity (IAM)
1.  Create an **IAM Role** for EC2 with the `AmazonS3FullAccess` policy.
2.  Attach this role to your EC2 instance. This allows the application to communicate with S3 securely without hardcoded credentials.

### 3. Storage Setup (S3)
1.  Create an S3 Bucket: `unievent-storage-ahmed-2026`.
2.  Keep "Block Public Access" enabled; the EC2 communicates via the internal AWS network using the IAM Role.

### 4. Server Configuration (EC2)
1.  Launch an **Amazon Linux 2023** instance.
2.  **Security Group:** Allow Inbound **HTTP (Port 80)** from the Load Balancer.
3.  Install dependencies:
    ```bash
    sudo yum update -y
    sudo yum install python3-pip -y
    pip3 install flask boto3 requests
    ```
4.  Run the data fetcher and start the server:
    ```bash
    python3 src/fetch_events.py
    sudo python3 src/app.py
    ```

### 5. High Availability (ALB)
1.  Create a **Target Group** (HTTP, Port 80) and register the EC2 instance.
2.  Create an **Application Load Balancer**, selecting both Public Subnets.
3.  Point the ALB Listener to your Target Group.

---

## 🔍 Technical Justification & Error Handling

### API Justification
I selected the **Ticketmaster Discovery API** because it provides highly structured, real-time JSON data. It allows the application to scale by pulling diverse event types (concerts, sports, lectures) through a single endpoint.

### Handling Inconsistent Data
During development, I encountered a `KeyError: 'classifications'` because Ticketmaster data is nested and inconsistent. I implemented a **Double-Safety Mechanism**:
1.  **Python Logic:** Used the `.get()` method in `app.py` to prevent crashes if the `_embedded` key is missing.
2.  **Jinja2 Templating:** Used `{% if %}` checks in `index.html` to provide a fallback value ("General Event") if specific categories are missing.


--- 

## 🖥️ Server Management & Directory Structure

### Root Access & Permissions
To host the application on the standard HTTP port (**Port 80**), administrative privileges were required. 
- **Elevation Command:** `sudo -i` was used to switch to the root user.
- **Port Management:** This allowed the Flask development server to bind to `0.0.0.0:80`, making it accessible to the Application Load Balancer.

### File System Organization
All application source code is centralized in the following directory on the EC2 instance:
- **Project Root:** `/home/ec2-user/unievent/`
- **Frontend Assets:** `/home/ec2-user/unievent/templates/`



### Running the Application
To ensure the application runs in the background and stays active after the terminal session ends, the following command was used:
```bash
# Navigate to the project folder
cd /home/ec2-user/unievent/

# Execute the application with root privileges
sudo python3 app.py
