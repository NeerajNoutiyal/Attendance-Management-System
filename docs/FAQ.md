# AttendFlow — Frequently Asked Questions

## 1. What is AttendFlow?

AttendFlow is a web-based Attendance Management System that helps manage student records and attendance.

## 2. Which technologies does the project use?

The project uses Python, Flask, SQLite, HTML, and CSS.

## 3. How do I run the application?

Install dependencies with `pip install -r requirements.txt`, configure the required environment variables, and run `python app.py`.

## 4. Why can't I log in?

Check that your username and password are correct. Administrators should also verify that the required environment variables are configured correctly.

## 5. Can I manage student records?

Authorized users can use the student-management features provided by the application.

## 6. How can I view attendance reports?

Open the report section and follow the available filters and reporting options.

## 7. Does the system prevent proxy attendance completely?

No. Authentication, student identification, and duplicate-entry checks can reduce unauthorized or duplicate entries, but they cannot guarantee that proxy attendance is impossible.

## 8. What should I do if the application crashes?

Check the terminal output for error messages. Confirm that dependencies are installed and the required environment variables are set.

## 9. Where is attendance data stored?

The current application uses an SQLite database. Keep the database protected and do not commit private attendance records to a public repository.

## 10. How can I contribute?

Review the project README, make a focused improvement, test it, and submit a meaningful Git commit.

## 11. Where can I find more instructions?

See [`README.md`](../README.md) and the [User Manual](USER_MANUAL.md).
