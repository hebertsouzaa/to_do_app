import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = "to_do.sqlite3"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subtitle TEXT,
            description TEXT,
            priority INTEGER DEFAULT 0
        )
        """)

@app.route("/")
def index():
    with sqlite3.connect(DB) as conn:
        tasks = conn.execute("SELECT id, title, subtitle, description, priority FROM tasks ORDER BY id DESC").fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    subtitle = request.form.get("subtitle")
    description = request.form.get("description")
    if title:
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO tasks (title, subtitle, description) VALUES (?, ?, ?)",
                         (title, subtitle, description))
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    return redirect(url_for("index"))

@app.route("/priority/<int:task_id>", methods=["POST"])
def priority(task_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("UPDATE tasks SET priority = CASE priority WHEN 0 THEN 1 ELSE 0 END WHERE id=?", (task_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
