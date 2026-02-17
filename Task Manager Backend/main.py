from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT
)
""")
conn.commit()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temporary in-memory storage
tasks = []
task_id_counter = 1

# data model (what frontend sends)
class Task(BaseModel):
    title: str
    description: str

@app.post("/tasks")
def create_task(task: Task):
    cursor.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
        (task.title, task.description, "todo")
    )
    conn.commit()

    task_id = cursor.lastrowid

    return {
        "message": "Task created",
        "task": {
            "id": task_id,
            "title": task.title,
            "description": task.description,
            "status": "todo"
        }
    }
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT id, title, description, status FROM tasks")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3]
        })

    return tasks
class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, status = ?
        WHERE id = ?
        """,
        (
            updated_task.title,
            updated_task.description,
            updated_task.status,
            task_id
        )
    )
    conn.commit()

    if cursor.rowcount == 0:
        return {"error": "Task not found"}

    return {
        "message": "Task updated",
        "task": {
            "id": task_id,
            "title": updated_task.title,
            "description": updated_task.description,
            "status": updated_task.status
        }
    }
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    if cursor.rowcount == 0:
        return {"error": "Task not found"}
    
    return {"message": "Task deleted"}