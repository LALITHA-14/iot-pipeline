# 🚀 IoT Sensor Data Pipeline (Event-Driven Architecture)

## 📌 Project Overview

This project implements an **event-driven IoT data pipeline** that simulates sensor data generation, publishes messages using **Google Cloud Pub/Sub Emulator**, processes them asynchronously through a consumer service, and stores results in **MySQL**.

The system demonstrates real-world **data engineering concepts** such as asynchronous messaging, containerization, and scalable microservice communication.

---

## 🏗️ Architecture

```
Producer → Pub/Sub Emulator → Consumer → MySQL Database
```

### Components

* **Producer Service**

  * Simulates IoT sensor readings
  * Publishes messages to Pub/Sub topic

* **Pub/Sub Emulator**

  * Local message broker
  * Enables event-driven communication without cloud dependency

* **Consumer Service**

  * Subscribes to messages
  * Processes incoming sensor data
  * Inserts records into MySQL

* **MySQL Database**

  * Stores processed sensor readings

---

## ⚙️ Tech Stack

* Python
* Docker & Docker Compose
* Google Cloud Pub/Sub Emulator
* MySQL 8.0
* Event-Driven Architecture
* REST & Messaging Concepts

---

## 📂 Project Structure

```
iot-pipeline/
│   .env.example
│   .gitignore
│   db_init.sql
│   docker-compose.yml
│   gcloud
│   publish.py
│   pubsub_init.py
│   README.md
│   setup_pubsub.py
│
├───consumer
│       app.py
│       Dockerfile
│       requirements.txt
│
└───producer
        app.py
        Dockerfile
        requirements.txt
```

---

## 🚀 Setup & Execution

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd iot-pipeline
```

---

### 2️⃣ Start Services

```bash
docker compose up -d --build
```

This starts:

* Producer container
* Consumer container
* MySQL database
* Pub/Sub Emulator

---

### 3️⃣ Verify Running Containers

```bash
docker ps
```

---

### 4️⃣ Publish Sensor Data

```bash
python publish.py
```

This sends simulated IoT readings to the Pub/Sub topic.

---

### 5️⃣ Check Consumer Logs

```bash
docker compose logs consumer
```

Expected output:

```
Listening for messages...
Received message
Inserted into MySQL
```

---

### 6️⃣ Verify Data in MySQL

```bash
docker exec -it iot-pipeline-mysql-1 mysql -u root -p
```

Inside MySQL:

```sql
USE iot_data;
SELECT * FROM sensor_readings;
```

---

## 🧠 Key Concepts Demonstrated

* Event-Driven Microservices
* Asynchronous Message Processing
* Pub/Sub Messaging Pattern
* Containerized Development
* Service Decoupling
* Fault-Tolerant Communication

---

## 🔄 Data Flow

1. Producer generates sensor readings.
2. Data published to Pub/Sub topic.
3. Consumer subscribes asynchronously.
4. Messages processed and validated.
5. Data stored in MySQL database.

---

## ✅ Features

* Fully containerized environment
* Local cloud emulator usage
* Asynchronous processing
* Automatic database persistence
* Scalable architecture design

---

## 📈 Future Improvements

* Add Airflow orchestration
* Real-time dashboard visualization
* Data validation layer
* Monitoring & logging integration
* Cloud deployment (GCP/AWS)

---

## 👨‍💻 Author

**IoT Event-Driven Data Pipeline Project**
Built as part of a data engineering learning workflow demonstrating practical distributed system design.

---

## 📜 License

This project is for educational and demonstration purposes.
