
import csv
import os
import secrets
import sqlite3
from datetime import date
from functools import wraps
from io import StringIO
from pathlib import Path

from flask import (
    Flask, Response, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

# Initialize the Flask application.
app = Flask(__name__)

# Load the secret key from the environment to protect session data.
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Configure session-cookie security options.
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

# Load administrator credentials from environment variables.
# The password must be stored as a secure hash, not plain text.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")

# Stop startup if the secret key has not been configured.
if not app.secret_key:
    raise RuntimeError(
        "FLASK_SECRET_KEY is missing. Configure it in your environment."
    )

# Store the SQLite database beside this Python file.
DB_PATH = Path(__file__).with_name("attendance.db")


# --------------------------------------------------
# 2. DATABASE CONNECTION AND INITIALIZATION
# --------------------------------------------------

def get_db():
    """Create and configure a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)

    # Return rows that can be accessed by column name.
    connection.row_factory = sqlite3.Row

    # Enable foreign-key validation for this connection.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_db():
    """Create the required database tables if they do not exist."""
    with get_db() as db:

        # Store each student's basic information.
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL
            )
        """)

        # Store daily attendance and prevent duplicate records
        # for the same student on the same date.
        db.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
                UNIQUE(student_id, date),
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        # Store student password hashes separately from student details.
        db.execute("""
            CREATE TABLE IF NOT EXISTS student_accounts (
                student_id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)


# Ensure the required tables exist before serving requests.
initialize_db()


# --------------------------------------------------
# 3. ROLE-BASED ACCESS CONTROL
# --------------------------------------------------

def admin_required(view_function):
    """Restrict a route to authenticated administrators."""
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        # Check the role stored in the authenticated session.
        if session.get("role") != "admin":

            # Redirect logged-in students to their own report.
            if session.get("role") == "student":
                return redirect(url_for("student_report"))

            # Unauthenticated users must log in.
            return redirect(url_for("login"))

        return view_function(*args, **kwargs)

    return wrapped_view


def student_required(view_function):
    """Restrict a route to authenticated students."""
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        # Prevent users without a student session from accessing the route.
        if session.get("role") != "student":
            return redirect(url_for("login"))

        return view_function(*args, **kwargs)

    return wrapped_view


# --------------------------------------------------
# 4. LOGIN AND AUTHENTICATION
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate administrators, teachers, and students."""

    # Send already-authenticated users to their relevant page.
    if session.get("role") == "admin":
        return redirect(url_for("index"))

    if session.get("role") == "student":
        return redirect(url_for("student_report"))

    if request.method == "POST":

        # Read the submitted login details.
        role = request.form.get("role", "admin").strip().lower()
        user_id = request.form.get("user_id", "").strip()
        password = request.form.get("password", "")

        if role in ("admin", "teacher"):

            # Admin and Teacher share one dashboard and the same credentials.
            if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
                flash(
                    "Admin login is not configured. Contact the administrator.",
                    "error"
                )
                return render_template("login.html"), 503

            # Compare the submitted password against the configured hash.
            if (
                user_id == ADMIN_USERNAME
                and check_password_hash(ADMIN_PASSWORD_HASH, password)
            ):
                # Clear previous session values before setting the admin role.
                session.clear()
                session["role"] = "admin"
                session["admin_logged_in"] = True

                return redirect(url_for("index"))

        elif role == "student":

            # Find the student account using the registered roll number.
            with get_db() as db:
                student = db.execute(
                    "SELECT s.id, a.password_hash FROM students s "
                    "JOIN student_accounts a ON a.student_id = s.id "
                    "WHERE s.roll_no = ?",
                    (user_id,)
                ).fetchone()

            # Verify the password hash before creating a student session.
            if (
                student
                and check_password_hash(student["password_hash"], password)
            ):
                session.clear()
                session["role"] = "student"
                session["student_id"] = student["id"]

                return redirect(url_for("student_report"))

        # Use a general error message for invalid login details.
        flash("Invalid ID or password.", "error")

    # Display the login page for GET requests or failed logins.
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    """Clear the current session and return to the login page."""

    # Remove the current user's session data.
    session.clear()

    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# --------------------------------------------------
# 5. ADMIN DASHBOARD AND ATTENDANCE OVERVIEW
# --------------------------------------------------

@app.route("/")
@admin_required
def index():
    """Display students, attendance records, and daily statistics."""

    # Read optional date and search filters from the URL.
    today = date.today().isoformat()
    selected_date = request.args.get("date", "").strip()
    search = request.args.get("search", "").strip()

    with get_db() as db:

        # Retrieve student details and indicate whether each has an account.
        students = db.execute("""
            SELECT s.*, CASE WHEN a.student_id IS NULL THEN 0 ELSE 1 END AS has_account
            FROM students s LEFT JOIN student_accounts a ON a.student_id = s.id
            ORDER BY s.name
        """).fetchall()

        # Build the attendance query using parameterized SQL.
        # Optional filters are added only when the user supplies them.
        query = """
            SELECT a.date, a.status, s.name, s.roll_no
            FROM attendance a JOIN students s ON s.id = a.student_id
            WHERE 1=1
        """
        params = []

        if selected_date:
            query += " AND a.date = ?"
            params.append(selected_date)

        if search:
            query += " AND (s.name LIKE ? OR s.roll_no LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])

        # Show the most recent records first and limit the displayed results.
        query += " ORDER BY a.date DESC, s.name LIMIT 100"
        records = db.execute(query, params).fetchall()

        # Calculate the daily counts shown on the dashboard.
        total_students = db.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        present_today = db.execute(
            "SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'Present'",
            (today,)
        ).fetchone()[0]

        absent_today = db.execute(
            "SELECT COUNT(*) FROM attendance WHERE date = ? AND status = 'Absent'",
            (today,)
        ).fetchone()[0]

    # Calculate today's attendance rate, avoiding division by zero.
    attendance_rate = (
        round(present_today / total_students * 100, 2)
        if total_students else 0
    )

    # Pass dashboard data to the HTML template.
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


# --------------------------------------------------
# 6. ADD A STUDENT AND CREATE A LOGIN ACCOUNT
# --------------------------------------------------

@app.route("/add_student", methods=["POST"])
@admin_required
def add_student():
    """Create a student record and its associated login account."""

    # Read and trim the student details submitted through the form.
    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    course = request.form.get("course", "").strip()
    password = request.form.get("student_password", "").strip()

    # Reject submissions missing required student information.
    if not name or not roll_no or not course:
        flash("Please fill in all student fields.", "error")
        return redirect(url_for("index"))

    # Generate a temporary password when none is supplied.
    # The existing application displays this password once after creation.
    temporary_password = None

    if not password:
        temporary_password = secrets.token_urlsafe(9)
        password = temporary_password

    try:
        with get_db() as db:

            # Insert the student and retrieve the newly created database ID.
            cursor = db.execute(
                "INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
                (name, roll_no, course)
            )
            student_id = cursor.lastrowid

            # Store only a password hash, never the plain-text password.
            db.execute(
                "INSERT INTO student_accounts (student_id, password_hash) VALUES (?, ?)",
                (student_id, generate_password_hash(password))
            )

        # Inform the administrator about the new account.
        if temporary_password:
            flash(
                f"Student added. Student ID: {roll_no}. Temporary password (save it now): "
                f"{temporary_password}",
                "success"
            )
        else:
            flash(
                f"Student added and login created for {roll_no}.",
                "success"
            )

    # A unique roll number is enforced by the database.
    except sqlite3.IntegrityError:
        flash("That roll number already exists.", "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# 7. EDIT STUDENT DETAILS
# --------------------------------------------------

@app.route("/edit_student/<int:student_id>", methods=["POST"])
@admin_required
def edit_student(student_id):
    """Update an existing student's name, roll number, and course."""

    # Read the updated values from the submitted form.
    name = request.form.get("name", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    course = request.form.get("course", "").strip()

    # Require all student fields before updating the database.
    if not name or not roll_no or not course:
        flash("All student fields are required.", "error")
        return redirect(url_for("index"))

    try:
        with get_db() as db:

            # Update only the student identified by the supplied database ID.
            cursor = db.execute(
                "UPDATE students SET name = ?, roll_no = ?, course = ? WHERE id = ?",
                (name, roll_no, course, student_id)
            )

            # Report whether a matching student was found.
            if cursor.rowcount == 0:
                flash("Student not found.", "error")
            else:
                flash("Student details updated successfully!", "success")

    # Prevent assigning a roll number already used by another student.
    except sqlite3.IntegrityError:
        flash("That roll number is already assigned to another student.", "error")

    return redirect(url_for("index"))


# --------------------------------------------------
# 8. DELETE A STUDENT
# --------------------------------------------------

@app.route("/delete_student/<int:student_id>", methods=["POST"])
@admin_required
def delete_student(student_id):
    """Delete a student and the student's attendance records."""

    with get_db() as db:

        # Delete related attendance entries before deleting the student.
        db.execute(
            "DELETE FROM attendance WHERE student_id = ?",
            (student_id,)
        )

        cursor = db.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    # Show a suitable message depending on whether the student existed.
    flash(
        "Student and their attendance records deleted."
        if cursor.rowcount else "Student not found.",
        "success" if cursor.rowcount else "error"
    )

    return redirect(url_for("index"))


# --------------------------------------------------
# 9. MARK OR UPDATE DAILY ATTENDANCE
# --------------------------------------------------

@app.route("/mark_attendance", methods=["POST"])
@admin_required
def mark_attendance():
    """Record a student's Present or Absent status for today."""

    # Read the student ID and attendance status from the form.
    student_id = request.form.get("student_id", type=int)
    status = request.form.get("status", "")

    # Validate the submitted ID and allowed attendance values.
    if not student_id or status not in ("Present", "Absent"):
        flash("Invalid attendance details.", "error")
        return redirect(url_for("index"))

    with get_db() as db:

        # Confirm that the selected student exists.
        student = db.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

        if student is None:
            flash("Student not found.", "error")
            return redirect(url_for("index"))

        # Insert today's attendance.
        # If a record already exists for this student and date,
        # update its status instead of creating a duplicate row.
        db.execute("""
            INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)
            ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status
        """, (student_id, date.today().isoformat(), status))

    flash(f"Attendance marked: {status}.", "success")
    return redirect(url_for("index"))


# --------------------------------------------------
# 10. STUDENT ATTENDANCE REPORT
# --------------------------------------------------

@app.route("/student_report")
def student_report():
    """Display an individual attendance report to an authorized user."""

    role = session.get("role")

    # Only authenticated administrators and students may view reports.
    if role not in ("admin", "student"):
        return redirect(url_for("login"))

    # Set default report values in case no student has been selected.
    report = []
    student = None
    total_days = present_days = absent_days = 0
    attendance_percentage = 0

    with get_db() as db:

        if role == "student":

            # A student can view only the account linked to their session.
            # Do not trust a student ID supplied in the URL.
            student = db.execute(
                "SELECT id, name, roll_no, course FROM students WHERE id = ?",
                (session.get("student_id"),)
            ).fetchone()

            students = [student] if student else []

        else:

            # Administrators can select from the available student records.
            students = db.execute(
                "SELECT id, name, roll_no, course FROM students ORDER BY name"
            ).fetchall()

            # Allow an administrator to locate a report by roll number.
            roll_no = request.args.get("roll_no", "").strip()

            if roll_no:
                student = db.execute(
                    "SELECT id, name, roll_no, course FROM students WHERE roll_no = ?",
                    (roll_no,)
                ).fetchone()

        # Retrieve and summarize attendance for the selected student.
        if student:
            report = db.execute(
                "SELECT date, status FROM attendance WHERE student_id = ? ORDER BY date DESC",
                (student["id"],)
            ).fetchall()

            total_days = len(report)
            present_days = sum(
                1 for row in report if row["status"] == "Present"
            )
            absent_days = sum(
                1 for row in report if row["status"] == "Absent"
            )

            # Calculate the percentage only when records are available.
            if total_days:
                attendance_percentage = round(
                    present_days / total_days * 100, 2
                )

    # Send the report and its summary statistics to the template.
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


# --------------------------------------------------
# 11. EXPORT ATTENDANCE REPORT TO CSV
# --------------------------------------------------

@app.route("/export_attendance")
@admin_required
def export_attendance():
    """Export attendance records as a downloadable CSV file."""

    # Create an in-memory text buffer instead of a temporary file.
    output = StringIO()
    writer = csv.writer(output)

    # Write the column headings first.
    writer.writerow(["Date", "Student Name", "Roll Number", "Course", "Status"])

    with get_db() as db:

        # Retrieve attendance records together with student information.
        records = db.execute("""
            SELECT a.date, s.name, s.roll_no, s.course, a.status
            FROM attendance a JOIN students s ON s.id = a.student_id
            ORDER BY a.date DESC, s.name
        """).fetchall()

        # Write each attendance record as a CSV row.
        for record in records:
            writer.writerow([
                record["date"],
                record["name"],
                record["roll_no"],
                record["course"],
                record["status"]
            ])

    # Add a UTF-8 BOM to help spreadsheet programs recognize text encoding.
    # Return the CSV as a file attachment in the HTTP response.
    return Response(
        "\ufeff" + output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=attendance_report.csv"
        }
    )


# --------------------------------------------------
# 12. APPLICATION ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    # Start the Flask development server when this file runs directly.
    # Debug mode remains disabled, as in the original application.
    app.run(host="0.0.0.0", port=5000, debug=False)
