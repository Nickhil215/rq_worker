# worker_task.py

import time

def long_running_task(value: int):
    """Simulate a slow CPU-bound task."""
    time.sleep(5)  # simulate work
    return {"input": value, "output": value * 2}
