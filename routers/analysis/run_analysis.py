# A simple in-memory store for tasks
# Keys = task_id, Value = dict with status, progress, and result
TASKS = {}

def start_analysis_process(ticker:str, task_id: str):
    TASKS[task_id] = {
        "status": "Started Analysis",
        "progress": 0,
        "ticker": ticker,
    }

    print("Hello World")

    # Once done, update the status and store a "result"
    TASKS[task_id]["status"] = "completed"
