
# 📋 Attendance Management System — AttendFlow

> **Automate attendance tracking and minimize proxy entries.**

AttendFlow is a web-based Attendance Management System designed to simplify attendance tracking, organize student records, reduce manual work, and help prevent duplicate or unauthorized attendance entries.

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Objectives](#-objectives)
- [Attendance Workflow](#-attendance-workflow)
- [Proxy-Entry Prevention](#-proxy-entry-prevention)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Usage Guide](#-usage-guide)
- [Documentation](#-documentation)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Developer](#-developer)
- [License](#-license)

## 🎯 Overview

The Attendance Management System provides a centralized way to manage student attendance records.

The project aims to improve the accuracy, accessibility, and organization of attendance information through a simple web interface.

It uses Python and Flask for application logic and SQLite for database storage.

## 🚀 Features

- 👨‍🎓 Student record management
- 🔐 Admin authentication
- 🔑 Student account authentication
- 📅 Attendance record management
- ⏰ Automatic date and time recording where implemented
- 🚫 Duplicate attendance prevention where implemented
- 📊 Attendance percentage calculation
- 📈 Attendance reports
- 📁 CSV export for supported reports
- 🔎 Organized attendance records
- 🌐 Web-based user interface
- 📖 User documentation and troubleshooting guides

*Note: Available features depend on the current implementation and user permissions.*

## 🎯 Objectives

1. Automate attendance tracking.
2. Reduce manual record-keeping.
3. Minimize duplicate and unauthorized entries.
4. Maintain organized student attendance records.
5. Calculate attendance percentages accurately.
6. Provide clear instructions for users.
7. Improve the maintainability of the application through documentation.

## 🔄 Attendance Workflow

```text
        Start
          |
          v
   Open Application
          |
          v
    User Login
          |
          v
   Authentication
          |
          v
 Access Authorized Features
          |
          v
 Manage Attendance Records
          |
          v
 Calculate Attendance Percentage
          |
          v
 View Reports / Export CSV
          |
          v
         End
```

## 🛡️ Proxy-Entry Prevention

The system can help reduce attendance errors and unauthorized entries through appropriate controls, such as:

- Authentication before accessing protected features.
- Unique student identification.
- Duplicate-entry checks.
- Date and time recording.
- Restricted access to administrative functions.
- Attendance record verification.

These controls can reduce the risk of proxy attendance, but they cannot guarantee that proxy attendance is impossible.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML | Web page structure |
| CSS | Web page styling |
| Git | Version control |
| GitHub | Source code hosting |
| Gunicorn | Production application server, where configured |

## 📂 Project Structure

```text
Attendance-Management-System/
├── .github/
│   └── workflows/
├── android-app/
├── docs/
│   ├── USER_MANUAL.md
│   ├── FAQ.md
│   └── ABOUT.md
├── static/
├── templates/
├── tests/
├── app.py
├── requirements.txt
├── Procfile
└── README.md
```

This is a simplified overview. Refer to the actual repository for the current files and folders.

## ⚙️ Installation and Setup

### Prerequisites

Install the following software:

- Python 3
- Git
- Visual Studio Code (recommended)
- A modern web browser

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/NeerajNoutiyal/Attendance-Management-System.git
```

Navigate to the project directory:

```bash
cd Attendance-Management-System
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Configure the environment variables required by your application:

- `FLASK_SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD_HASH`

Use the actual configuration instructions in the source code and deployment settings.

**Security reminders:**

- Never commit passwords, secret keys, or other credentials to GitHub.
- Use a strong, unique secret key.
- Store the admin password as a secure hash where supported.
- Keep production credentials in the deployment platform's environment settings.

### 5. Run the Application

```bash
python app.py
```

Open the local address displayed in the terminal, typically:

```text
http://127.0.0.1:5000
```

The port may differ depending on the application configuration.

## 💻 Usage Guide

### Administrator

1. Start the application.
2. Open the application in a browser.
3. Navigate to the admin login page.
4. Enter the configured administrator credentials.
5. Open the admin dashboard.
6. Use the available student-management features.
7. Manage attendance records.
8. View attendance reports.
9. Export supported reports to CSV.

### Student

1. Open the application.
2. Navigate to the student login page, if available.
3. Enter your registered credentials.
4. Open the student dashboard.
5. View the attendance information available to your account.

The exact pages and available actions depend on the current implementation.

## 📖 Documentation

The following documents provide additional information about the project.

| Document | Description |
|---|---|
| [User Manual](docs/USER_MANUAL.md) | Step-by-step instructions for using the application |
| [FAQ / Help](docs/FAQ.md) | Frequently asked questions and troubleshooting |
| [About the Project](docs/ABOUT.md) | Project purpose, features, and technologies |

### Documentation Goals

- Make installation easier for new users.
- Explain the application workflow.
- Help users troubleshoot common problems.
- Describe the purpose and features of the project.
- Improve readability and maintainability.
- Keep documentation consistent with the actual application.

## ❓ Troubleshooting

| Problem | Suggested solution |
|---|---|
| Python command not recognized | Install Python and verify that it is added to PATH |
| Dependency installation fails | Check your internet connection and Python environment |
| Application does not start | Review the terminal error and verify the required dependencies |
| Admin login fails | Check the configured username and password hash |
| Database error occurs | Check the database path, permissions, and application configuration |
| Report is empty | Verify that student and attendance records exist |
| CSV export fails | Check the report route, permissions, and export implementation |
| Local page does not open | Confirm that the Flask application is running at the displayed address |

For more help, see the [FAQ](docs/FAQ.md) and [User Manual](docs/USER_MANUAL.md).

## 🔮 Future Enhancements

Possible future improvements include:

- QR-code-based attendance.
- Biometric integration.
- Optional face-recognition attendance.
- Improved attendance analytics.
- Email or SMS notifications.
- Additional report filters.
- Better mobile responsiveness.
- Automated testing for important workflows.
- Expanded user documentation.

These are proposed enhancements, not claims that these features are currently implemented.

## 👨‍💻 Developer

**Neeraj Noutiyal**

B.Tech — Computer Science Engineering (AI & ML)

GitHub: [NeerajNoutiyal](https://github.com/NeerajNoutiyal)

## 📄 License

This project was developed for educational and academic project purposes.

Refer to the repository for any applicable license file or additional usage conditions.
