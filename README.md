# rq_worker
Below is a **clean, professional, production-quality README.md** for your **FastAPI + Redis + RQ Worker** POC.

---

# 🚀 FastAPI + Redis RQ Worker — Proof of Concept

This project is a **minimal and clean POC** showing how to run **asynchronous background jobs** in FastAPI using:

* **FastAPI** — API layer
* **Redis** — message broker
* **RQ (Redis Queue)** — job queue + worker
* **Python worker** — executes long-running tasks outside the API process

This architecture is ideal for building **high-throughput, non-blocking, scalable applications**, especially for CPU/GPU-based workloads like ML inference, media processing, or scheduled tasks.

---

## 📁 Project Structure

```
.
├── main.py              # FastAPI server
├── worker_task.py       # Long-running task executed by worker
└── README.md            # This file
```

---

# ⚡ Quick Start

## 1️⃣ Install dependencies

```bash
pip install fastapi uvicorn redis rq
```

---

## 2️⃣ Start Redis

If you have Docker:

```bash
docker run -p 6379:6379 redis
```

Or install Redis manually if preferred.

---

## 3️⃣ Run FastAPI Server

```bash
uvicorn main:app --reload
```

API will run at:

```
http://localhost:8000
```

---

## 4️⃣ Start the RQ Worker

In another terminal:

```bash
rq worker -P .
```

`-P .` ensures it loads tasks from your project directory.

---

# 🧠 How It Works

### ✔ API does *not* execute long tasks

Instead, it pushes jobs into Redis Queue:

```bash
POST /run-task
```

FastAPI immediately returns a **job_id** so the client is not blocked.

---

### ✔ Worker pulls tasks from Redis

Running `rq worker` starts a process that:

1. Fetches jobs from the queue
2. Runs `long_running_task()`
3. Stores result back into Redis

---

### ✔ Client polls job status

```
GET /status/{job_id}
```

Responses:

| Status     | Meaning                             |
| ---------- | ----------------------------------- |
| `queued`   | Job is waiting in queue             |
| `started`  | Worker is processing the job        |
| `finished` | Job completed, result available     |
| `failed`   | Exception occurred during execution |

---

# 📌 API Endpoints

### **POST /run-task**

Submit a long-running job.

Example:

```
POST http://localhost:8000/run-task?value=10
```

Response:

```json
{
  "job_id": "1234-abcd-5678",
  "status": "queued"
}
```

---

### **GET /status/{job_id}**

Check whether your job is completed.

Example:

```
GET http://localhost:8000/status/1234-abcd-5678
```

Response:

```json
{
  "status": "finished",
  "result": {"input": 10, "output": 20}
}
```

---

# 🧪 Test Task Logic (worker_task.py)

```python
import time

def long_running_task(value: int):
    time.sleep(5)  # simulate slow work
    return {"input": value, "output": value * 2}
```

---

# 🚀 Scaling & Production Tips

### ✔ Run multiple workers for parallel job processing:

```bash
rq worker -P . &
rq worker -P . &
rq worker -P . &
```

### ✔ Use containerized Redis + worker + API

(easy to scale in Docker Swarm / Kubernetes)

### ✔ Make workers GPU-enabled for ML workloads

(e.g., PyTorch/TensorFlow diffusers models)

### ✔ Use `rq-dashboard` for monitoring

```bash
pip install rq-dashboard
rq-dashboard
```

Open:

```
http://localhost:9181
```

---

# 🎯 What This POC Demonstrates

* Non-blocking FastAPI behavior
* Job queueing with Redis
* Background processing with RQ worker
* Simple interface for polling job status
* Ready foundation for ML, video, or CPU/GPU heavy tasks

---
