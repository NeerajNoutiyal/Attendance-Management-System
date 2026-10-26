
# 📘 Attendance Management System — User Manual

## 1. Introduction

The Attendance Management System (AttendFlow) is a web-based application designed to organize student records, manage attendance, and review attendance reports.

This manual explains how to set up and use the application's available features.

## 2. System Requirements

- Python 3
- A modern web browser
- Required Python packages listed in `requirements.txt`
- Access to the project source code
- Configured application credentials

## 3. Installation and Setup

### Step 1: Open the Project

Open the project folder in Visual Studio Code or a terminal.

### Step 2: Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Configure the environment variables required by the application:

- `FLASK_SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD_HASH`

Use secure values and follow the configuration instructions in the project.

Never share passwords, password hashes, or secret keys publicly.

### Step 4: Start the Application

Run:

```bash
python app.py
```

Open the local URL displayed in the terminal. The default Flask development address is often `http://127.0.0.1:5000`.

## 4. Administrator Login

1. Open the application in your browser.
2. Navigate to the administrator login page.
3. Enter the configured administrator username and password.
4. Submit the login form.
5. After successful authentication, open the admin dashboard.

If login fails, verify your credentials and environment configuration. Do not publish secret values in issue reports or screenshots.

## 5. Student Management

If student management is enabled in your application:

1. Log in as an administrator.
2. Open the student management section.
3. Use the available form to add or update student information.
4. Verify the entered information before saving.
5. Review the student list to confirm the changes.

Use the application's available controls to manage or remove records, where supported.

## 6. Student Login

If student accounts are enabled:

1. Open the student login page.
2. Enter the registered student credentials.
3. Submit the login form.
4. View the attendance information available to your account.

Students should not use administrator credentials.

## 7. Attendance Management

1. Log in with an account authorized to manage attendance.
2. Open the attendance section.
3. Select the relevant student or available attendance options.
4. Enter or select the required attendance information.
5. Submit the form.
6. Check the attendance records to verify the result.

The exact workflow depends on the attendance features implemented in the current application.

## 8. Attendance Reports

1. Open the reports or student report section.
2. Select the available student or reporting options.
3. Review the attendance records.
4. Check the displayed attendance percentage, if available.
5. Verify the records before using them for academic decisions.

Attendance percentages should be based on the application's actual attendance calculation rules.

## 9. Exporting Attendance to CSV

If CSV export is available:

1. Open the relevant attendance report.
2. Select the CSV export option.
3. Save the downloaded file.
4. Open it in Microsoft Excel or another spreadsheet application.
5. Check that the exported records match the report.

Store exported student information securely and share it only with authorized people.

## 10. Logging Out

Use the application's logout option when you finish your work.

Always log out when using a shared computer.

## 11. Troubleshooting

| Problem | Suggested solution |
|---|---|
| Application does not start | Check Python installation and terminal errors |
| Missing Python package | Run `pip install -r requirements.txt` |
| Administrator login fails | Check the configured username and password |
| Student login fails | Verify the student account and credentials |
| Student records are missing | Check the database and confirm that the records were saved |
| Attendance is incorrect | Review the stored attendance records and calculation rules |
| CSV export fails | Check the export feature and browser download settings |
| Local website does not open | Confirm that the application is running and use its displayed URL |

## 12. Security Guidelines

- Never commit passwords or secret keys to GitHub.
- Use strong credentials.
- Do not share administrator accounts.
- Protect exported attendance records.
- Log out after using a shared computer.
- Keep dependencies and application code maintained.

## 13. Help and Support

For common questions, consult [FAQ.md](FAQ.md).

For information about the project's purpose and technologies, see [ABOUT.md](ABOUT.md).

## 14. Conclusion

This manual provides general instructions for setting up and using AttendFlow.

Available features and navigation may vary according to the current implementation. Keep this document updated whenever application functionality changes.
