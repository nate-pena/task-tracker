from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
import uuid

# Create the FastAPI app
app = FastAPI(title="Task Tracker API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file path
DATA_FILE = "tasks.json"

# Task model
class TaskBase(BaseModel):
    text: str
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    created_at: str

# Helper functions for data persistence
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# API Routes
@app.get("/")
def read_root():
    return {"message": "Task Tracker API is running"}

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return load_tasks()

@app.post("/api/tasks", response_model=Task)
def create_task(task: TaskCreate):
    tasks = load_tasks()
    
    new_task = Task(
        id=str(uuid.uuid4()),
        text=task.text,
        completed=task.completed,
        created_at=datetime.now().isoformat()
    )
    
    tasks.append(new_task.dict())
    save_tasks(tasks)
    
    return new_task

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: TaskBase):
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[i]["text"] = updated_task.text
            tasks[i]["completed"] = updated_task.completed
            save_tasks(tasks)
            return tasks[i]
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            return {"message": "Task deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Task not found")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
