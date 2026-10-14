
import csv
import sqlite3
from io import StringIO
from pathlib import Path
from datetime import date

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    flash
)

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

DB_PATH = Path(__file__).with_name("attendance.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
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
                status TEXT NOT NULL
                    CHECK(status IN ('Present', 'Absent')),
                UNIQUE(student_id, date),
                FOREIGN KEY(student_id)
                    REFERENCES students(id)
                    ON DELETE CASCADE
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
        round(present_today / total_students * 100, 2)
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
        flash("Please fill in all student fields.", "error")
        return redirect(url_for("index"))

    try:
        with get_db() as db:
            db.execute("""
                INSERT INTO students (name, roll_no, course)
                VALUES (?, ?, ?)
            """, (name, roll_no, course))

        flash("Student added successfully!", "success")

    except sqlite3.IntegrityError:
        flash("That roll number already exists.", "error")

    return redirect(url_for("index"))


@app.route("/edit_student/<int:student_id>", methods=["POST"])
def edit_student(student_id):
    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    course = request.form.get("course", "").strip()

    if not name or not roll_no or not course:
        flash("All student fields are required.", "error")
        return redirect(url_for("index"))

    try:
        with get_db() as db:
            cursor = db.execute("""
                UPDATE students
                SET name = ?, roll_no = ?, course = ?
                WHERE id = ?
            """, (name, roll_no, course, student_id))

            if cursor.rowcount == 0:
                flash("Student not found.", "error")
            else:
                flash("Student details updated successfully!", "success")

    except sqlite3.IntegrityError:
        flash("That roll number is already assigned to another student.", "error")

    return redirect(url_for("index"))


@app.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            flash("Student not found.", "error")
        else:
            flash(
                "Student and their attendance records deleted.",
                "success"
            )

    return redirect(url_for("index"))


@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    student_id = request.form.get("student_id", type=int)
    status = request.form.get("status", "")

    if not student_id or status not in ("Present", "Absent"):
        flash("Invalid attendance details.", "error")
        return redirect(url_for("index"))

    with get_db() as db:
        student = db.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

        if student is None:
            flash("Student not found.", "error")
            return redirect(url_for("index"))

        db.execute("""
            INSERT INTO attendance (student_id, date, status)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, date)
            DO UPDATE SET status = excluded.status
        """, (student_id, date.today().isoformat(), status))

    flash(f"Attendance marked: {status}.", "success")
    return redirect(url_for("index"))


@app.route("/student_report")
def student_report():
    roll_no = request.args.get("roll_no", "").strip()

    report = []
    student = None
    total_days = 0
    present_days = 0
    absent_days = 0
    attendance_percentage = 0

    with get_db() as db:
        students = db.execute("""
            SELECT id, name, roll_no, course
            FROM students
            ORDER BY name
        """).fetchall()

        if roll_no:
            student = db.execute("""
                SELECT id, name, roll_no, course
                FROM students
                WHERE roll_no = ?
            """, (roll_no,)).fetchone()

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

                if total_days:
                    attendance_percentage = round(
                        present_days / total_days * 100, 2
                    )

    return render_template(
        "student_report.html",
        students=students,
        student=student,
        report=report,
        total_days=total_days,
        present_days=present_days,
        absent_days=absent_days,
        attendance_percentage=attendance_percentage
    )


@app.route("/export_attendance")
def export_attendance():
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Date", "Student Name", "Roll Number", "Course", "Status"
    ])

    with get_db() as db:
        records = db.execute("""
            SELECT a.date, s.name, s.roll_no, s.course, a.status
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            ORDER BY a.date DESC, s.name
        """).fetchall()

        for record in records:
            writer.writerow([
                record["date"],
                record["name"],
                record["roll_no"],
                record["course"],
                record["status"]
            ])

    return Response(
        "\ufeff" + output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=attendance_report.csv"
        }
    )


if __name__ == "__main__":
    initialize_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
