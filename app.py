from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "tasks.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
        (title, description, priority)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
