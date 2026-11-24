import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from html import escape

app = FastAPI(title="student-task-tracker")

APP_TITLE = os.environ.get("APP_TITLE", "Task Flow - Student Task Tracker")

# List of student tasks
TASKS = [
    {"id": 1, "title": "Complete Docker Lab", "completed": False},
    {"id": 2, "title": "Study for Final Exam", "completed": False},
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/tasks")
def list_tasks():
    return {"tasks": TASKS}


@app.get("/", response_class=HTMLResponse)
def home():
    task_list = ""

    for task in TASKS:
        title = escape(task["title"])

        if task["completed"]:
            task_list += f"<li>{title} - Completed</li>"
        else:
            task_list += f"""
            <li>
                {title}
                <form action="/complete/{task['id']}" method="post">
                    <button>Mark Complete</button>
                </form>
            </li>
            """

    return f"""
    <html>
    <head>
        <title>Task Flow</title>
    </head>
    <body style="font-family: Arial; margin: 40px; background-color: #f1f5f9;">
        <h1>{escape(APP_TITLE)}</h1>
        <p>Keep track of your assignments and responsibilities.</p>

        <form action="/add" method="post">
            <input name="title" placeholder="Enter a task" required>
            <button>Add Task</button>
        </form>

        <h2>My Tasks</h2>
        <ul>{task_list}</ul>
    </body>
    </html>
    """


@app.post("/add")
def add_task(title: str = Form(...)):
    if title.strip():
        TASKS.append({
            "id": len(TASKS) + 1,
            "title": title.strip(),
            "completed": False
        })

    return RedirectResponse("/", status_code=303)


@app.post("/complete/{task_id}")
def complete_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            task["completed"] = True

    return RedirectResponse("/", status_code=303)
