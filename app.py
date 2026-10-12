
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("attendance.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
                UNIQUE(student_id, date),
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)


@app.route("/")
def index():
    today = date.today().isoformat()
    selected_date = request.args.get("date", "").strip()
    search = request.args.get("search", "").strip()

    with get_db() as db:
        students = db.execute(
            "SELECT * FROM students ORDER BY name"
        ).fetchall()

        query = """
            SELECT a.date, a.status, s.name, s.roll_no
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            WHERE 1=1
        """
        params = []

        if selected_date:
            query += " AND a.date = ?"
            params.append(selected_date)

        if search:
            query += " AND (s.name LIKE ? OR s.roll_no LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])

        query += " ORDER BY a.date DESC, s.name LIMIT 100"
        records = db.execute(query, params).fetchall()

        total_students = db.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        present_today = db.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE date = ? AND status = 'Present'
        """, (today,)).fetchone()[0]

        absent_today = db.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE date = ? AND status = 'Absent'
        """, (today,)).fetchone()[0]

    attendance_rate = (
        round(present_today / total_students * 100)
        if total_students else 0
    )

    return render_template(
        "index.html",
        students=students,
        records=records,
        total_students=total_students,
        present_today=present_today,
        absent_today=absent_today,
        attendance_rate=attendance_rate,
        selected_date=selected_date,
        search=search
    )


@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    course = request.form.get("course", "").strip()

    if not name or not roll_no or not course:
        return "All student fields are required.", 400

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
                (name, roll_no, course)
            )
    except sqlite3.IntegrityError:
        return "That roll number already exists.", 400

    return redirect(url_for("index"))


@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    student_id = request.form.get("student_id", type=int)
    status = request.form.get("status", "")

    if not student_id or status not in ("Present", "Absent"):
        return "Invalid attendance details.", 400

    with get_db() as db:
        student = db.execute(
            "SELECT id FROM students WHERE id = ?", (student_id,)
        ).fetchone()

        if student is None:
            return "Student not found.", 404

        db.execute("""
            INSERT INTO attendance (student_id, date, status)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, date)
            DO UPDATE SET status = excluded.status
        """, (student_id, date.today().isoformat(), status))

    return redirect(url_for("index"))

@app.route("/student_report")
def student_report():
    roll_no = request.args.get("roll_no", "").strip()
    report = []
    student = None
    total_days = 0
    present_days = 0
    absent_days = 0

    with get_db() as db:
        students = db.execute(
            "SELECT id, name, roll_no, course FROM students ORDER BY name"
        ).fetchall()

        if roll_no:
            student = db.execute(
                "SELECT id, name, roll_no, course FROM students WHERE roll_no = ?",
                (roll_no,)
            ).fetchone()

            if student:
                report = db.execute("""
                    SELECT date, status
                    FROM attendance
                    WHERE student_id = ?
                    ORDER BY date DESC
                """, (student["id"],)).fetchall()

                total_days = len(report)
                present_days = sum(
                    1 for record in report
                    if record["status"] == "Present"
                )
                absent_days = sum(
                    1 for record in report
                    if record["status"] == "Absent"
                )

    return render_template(
        "student_report.html",
        students=students,
        student=student,
        report=report,
        total_days=total_days,
        present_days=present_days,
        absent_days=absent_days
    )


if __name__ == "__main__":
    initialize_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
