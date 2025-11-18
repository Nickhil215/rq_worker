# main.py

from fastapi import FastAPI
from redis import Redis
from rq import Queue
import uuid
import os

# Redis connection
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis = Redis.from_url(redis_url)
q = Queue(connection=redis)

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/run-task")
async def run_task(value: int):
    job_id = str(uuid.uuid4())
    job = q.enqueue("worker_task.long_running_task", value, job_id=job_id)
    return {"job_id": job.get_id(), "status": "queued"}


@app.get("/status/{job_id}")
async def status(job_id: str):
    job = q.fetch_job(job_id)

    if job is None:
        return {"error": "job not found"}

    if job.is_finished:
        return {"status": "finished", "result": job.result}

    if job.is_failed:
        return {"status": "failed"}

    return {"status": job.get_status()}


# pip install python-dotenv
# pip install fastapi uvicorn redis rq
# pip install pydantic
