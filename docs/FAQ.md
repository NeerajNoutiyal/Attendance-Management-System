
# ❓ Frequently Asked Questions (FAQ)
## Attendance Management System — AttendFlow

This document answers common questions about installing, accessing, and using AttendFlow.

## 1. General Questions

### Q1. What is AttendFlow?

AttendFlow is a web-based Attendance Management System designed to organize student records, manage attendance, and review attendance reports.

### Q2. What is the purpose of this project?

The project aims to reduce manual attendance work, organize records, and make attendance information easier to manage.

### Q3. Which technologies does the project use?

The project uses Python, Flask, SQLite, HTML, and CSS.

### Q4. Who can use the application?

Administrators can access authorized management features. Students can access student features if student accounts and login functionality are enabled.

## 2. Installation and Setup

### Q5. How do I install the application?

Clone the repository, install the required packages, configure the required environment variables, and run the application.

See the [User Manual](USER_MANUAL.md) for detailed instructions.

### Q6. How do I install the Python dependencies?

Run this command in the project directory:

```bash
pip install -r requirements.txt
```

### Q7. How do I start the application?

Run:

```bash
python app.py
```

Then open the local URL displayed in the terminal.

### Q8. Why does the application fail to start?

Check that Python is installed, dependencies are available, required environment variables are configured, and the terminal does not report an error.

## 3. Login and Accounts

### Q9. What should I do if administrator login fails?

Check the configured administrator username and password. Confirm that the required environment variables are set correctly.

Never share your credentials publicly.

### Q10. What if student login fails?

Verify that the student account exists and that the entered credentials are correct. If the problem continues, ask the administrator to check the account.

### Q11. Can students access administrator features?

Students should only access features permitted by their account. Administrator routes must be protected by server-side authentication and authorization.

## 4. Attendance Management

### Q12. How do I manage attendance?

Sign in with an authorized account and open the attendance section. Follow the options available in your application to manage and verify attendance records.

### Q13. Can duplicate attendance entries occur?

The application may include duplicate-entry checks. Their effectiveness depends on the implemented validation rules and database constraints.

### Q14. How is attendance percentage calculated?

A common calculation is:

**Attendance Percentage = (Classes Attended ÷ Total Classes Held) × 100**

The actual result depends on how your application records attendance and defines the total classes.

### Q15. What should I do if attendance information is incorrect?

Review the stored attendance records and the applicable calculation rules. Correct records only through authorized application features.

## 5. Reports and CSV Export

### Q16. How do I view attendance reports?

Open the available reports section and select the student or reporting options supported by the application.

### Q17. How do I export attendance records?

If CSV export is enabled, open the relevant report and use the export option. Save the downloaded file and verify its contents.

### Q18. Why is my report empty?

Check whether student records and attendance data exist. Also verify the selected student, date filters, and report configuration, if applicable.

### Q19. Can I open a CSV file in Excel?

Yes. CSV files can be opened in Microsoft Excel and other spreadsheet applications.

## 6. Database and Security

### Q20. Where is attendance data stored?

The project uses SQLite. The database location depends on the application's configuration.

### Q21. How can I protect student information?

Use authorized accounts, protect credentials, restrict access to exported files, and avoid publishing private student information.

### Q22. Should I upload passwords to GitHub?

No. Keep passwords, secret keys, and other sensitive credentials out of the repository.

### Q23. How can I prevent unauthorized access?

Use secure authentication, enforce authorization on protected server routes, validate submitted data, and keep dependencies updated.

## 7. Troubleshooting

### Q24. What should I do if a required package is missing?

Activate the correct Python environment and run:

```bash
pip install -r requirements.txt
```

### Q25. Why can I not open the local website?

Confirm that the application is running and that you are using the URL and port shown in the terminal.

### Q26. What should I do if CSV export does not work?

Check that the export feature is available, review any error messages, and verify the browser's download settings.

### Q27. Where can I find detailed usage instructions?

Read the [User Manual](USER_MANUAL.md).

## 8. Additional Documentation

- [User Manual](USER_MANUAL.md) — Installation and usage instructions.
- [About the Project](ABOUT.md) — Project purpose, features, and technologies.

---

**Note:** Answers describe the intended behavior of AttendFlow. Exact options depend on the application's current implementation.
