from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid
from routers.analysis.run_analysis import TASKS, start_analysis_process

router = APIRouter()

@router.get("/generate-analysis")
def start_analysis(ticker:str, title: str, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())

    # Initialize the task in the store with "pending" or "starting"
    TASKS[task_id] = {
        "status": "pending",
        "progress": 0,
        "ticker": ticker
    }

    # Add the analysis function to the background tasks
    background_tasks.add_task(start_analysis_process, ticker, task_id)

    return {
        "message": f"Analysis for {ticker} started",
        "task_id": task_id,
        "status": "started"
    }

@router.get("/analysis-status")
def analysis_status(task_id: str):
    """
    Polling endpoint: user calls this with the task_id to check
    status and progress of the background job.
    """
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TASKS[task_id]