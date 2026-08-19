# 🧮 Vedic Mathematics Learning Platform

A **Vedic Mathematics Learning Platform** built with **Flask + MySQL** that helps students learn and practice the **16 Vedic Math Sutras**, improve calculation speed, take quizzes, track accuracy, and monitor their daily learning streaks.

---

## 📚 Features

* 👤 User Registration & Login
* 🔐 Secure password handling
* 📊 Student Dashboard
* 📈 Practice accuracy statistics
* 🎯 Track attempted and mastered Sutras
* 📖 Learn all **16 Vedic Math Sutras**
* 🧮 Step-by-step Sutra solvers
* ✍️ Live practice questions
* 📝 **55-question multiple-choice quiz**
* 💾 Auto-save quiz progress
* 🔄 Refresh-safe quiz progress
* 👤 Student Profile
* 📊 Combined Quiz + Practice statistics
* 🔥 Daily learning streak counter
* ✏️ Edit profile information
* 🖼️ Profile photo upload
* 🤖 AI Scan placeholder page
* ⚡ Speed Test placeholder page
* 📞 Contact page
* ❌ Custom 404 error page

---

# 🛠️ Tech Stack

### Backend

* Python 3.10+
* Flask
* MySQL
* mysql-connector-python
* python-dotenv
* Werkzeug

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Vanilla JavaScript

### Additional Libraries

* Google Generative AI
* Pillow

---

# 📋 Prerequisites

Before running the project, make sure you have the following installed:

### 1. Python

Python **3.10 or higher** is recommended.

Check your Python version:

```bash
python --version
```

You can download Python from:

https://www.python.org/

---

### 2. MySQL

You need a running MySQL server.

You can use:

* XAMPP
* WAMP
* MySQL Server
* MySQL Workbench

Check MySQL:

```bash
mysql --version
```

---

### 3. Git

If you are cloning the project from GitHub, install Git.

Check Git:

```bash
git --version
```

---

# 📁 Project Structure

The project structure should look approximately like this:

```text
Vedic-Maths/
│
├── app.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── quiz.html
│   ├── practice.html
│   ├── practice_details.html
│   ├── sutras.html
│   ├── sutra_detail.html
│   ├── ai_scan.html
│   ├── speed_test.html
│   ├── contact.html
│   └── 404.html
│
└── README.md
```

The `uploads/` directory is used for uploaded profile photos and can be created automatically by the application.

---

# 🚀 Installation & Setup

## Step 1 — Get the Project Files

Clone the project from GitHub:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project directory:

```bash
cd Vedic-Maths
```

Or, if you already have the project folder, simply open a terminal inside the project directory.

---

# Step 2 — Create a Virtual Environment

Creating a virtual environment is recommended.

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

After activation, you should see something similar to:

```text
(venv)
```

in your terminal.

---

# Step 3 — Install Python Dependencies

Install Flask:

```bash
pip install flask
```

Install MySQL connector:

```bash
pip install mysql-connector-python
```

Install Werkzeug:

```bash
pip install werkzeug
```

Install python-dotenv:

```bash
pip install python-dotenv
```

Install Google Generative AI:

```bash
pip install google-generativeai
```

Install Pillow:

```bash
pip install Pillow
```

### Or install everything together

You can install all required packages with:

```bash
pip install flask mysql-connector-python werkzeug python-dotenv google-generativeai Pillow
```

---

# Step 4 — MySQL Database Setup

Open:

* MySQL Workbench
* phpMyAdmin
* MySQL command line

Create the database:

```sql
CREATE DATABASE vedic_math;
```

Select the database:

```sql
USE vedic_math;
```

---

# Step 5 — Create the Students Table

Run:

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    profile_pic VARCHAR(255) DEFAULT 'default.png',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_active_date DATE NULL,
    current_streak INT NOT NULL DEFAULT 0
);
```

This table stores student registration, login, profile, and streak information.

---

# Step 6 — Create the Quizzes Table

Run:

```sql
CREATE TABLE quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    total_questions INT DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Insert the default quiz:

```sql
INSERT INTO quizzes (id, title)
VALUES (1, 'Vedic Mathematics Challenge');
```

The application uses `quiz_id = 1` for the main Vedic Mathematics quiz.

---

# Step 7 — Create the Quiz Attempts Table

Run:

```sql
CREATE TABLE quiz_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    quiz_id INT NOT NULL,
    current_question INT DEFAULT 1,
    total_questions INT DEFAULT 0,
    attempted_questions INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    wrong_answers INT DEFAULT 0,
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'in_progress',
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    FOREIGN KEY (quiz_id)
        REFERENCES quizzes(id)
        ON DELETE CASCADE
);
```

This table stores quiz progress and results.

---

# Step 8 — Create the Student Answers Table

This table stores individual answers given by students during the quiz.

```sql
CREATE TABLE student_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    quiz_id INT NOT NULL,
    question_index INT NOT NULL,
    selected_option VARCHAR(255) NOT NULL,
    is_correct TINYINT(1) NOT NULL DEFAULT 0,
    answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_student_quiz_question
        (student_id, quiz_id, question_index),

    FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);
```

The unique key prevents duplicate answers for the same student, quiz, and question.

---

# Step 9 — Create the Practice Answers Table

This table stores individual practice-question results.

```sql
CREATE TABLE practice_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    sutra_id INT NOT NULL,
    question_id INT NOT NULL,
    user_answer VARCHAR(255),
    correct_answer VARCHAR(255),
    is_correct TINYINT(1) NOT NULL DEFAULT 0,
    answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);
```

---

# ⚠️ Old `practice_results` Table

An older table named:

```text
practice_results
```

may exist from an earlier version of the project.

The current application uses:

```text
practice_answers
```

instead.

Therefore, `practice_results` can be ignored.

If you are sure that the old table is not required, it can be removed:

```sql
DROP TABLE practice_results;
```

---

# Step 10 — Verify Database Tables

Run:

```sql
SHOW TABLES;
```

You should see tables similar to:

```text
students
quizzes
quiz_attempts
student_answers
practice_answers
```

Check the quiz:

```sql
SELECT * FROM quizzes;
```

You should have:

```text
1 | Vedic Mathematics Challenge
```

---

# Step 11 — Configure Database Connection

Open:

```text
app.py
```

Find the database configuration:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vedic_math"
}
```

Update the values according to your MySQL configuration.

For example:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",
    "database": "vedic_math"
}
```

### If MySQL root has no password

Use:

```python
"password": ""
```

---

# 🔐 Optional — Using `.env`

If your project uses `python-dotenv`, you can keep configuration in a `.env` file.

Create:

```text
.env
```

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=vedic_math
```

If your application also uses Google Generative AI, you can add your API key:

```env
GEMINI_API_KEY=your_api_key_here
```

**Do not upload `.env` to GitHub.**

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
static/uploads/
```

---

# ▶️ Step 12 — Run the Application

From the project directory:

```bash
python app.py
```

You should see something similar to:

```text
 * Running on http://127.0.0.1:5000
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

# 🌐 Application Routes

| Route            | Purpose              |
| ---------------- | -------------------- |
| `/`              | Home page            |
| `/register`      | Student registration |
| `/login`         | Student login        |
| `/logout`        | Logout               |
| `/dashboard`     | Student dashboard    |
| `/sutras`        | View all 16 Sutras   |
| `/sutra/<id>`    | Sutra details        |
| `/practice/<id>` | Practice a Sutra     |
| `/quiz`          | 55-question quiz     |
| `/profile`       | Student profile      |
| `/ai-scan`       | AI Scan page         |
| `/speed-test`    | Speed Test page      |
| `/contact`       | Contact page         |

---

# 📖 16 Vedic Mathematics Sutras

The platform provides learning and practice for the 16 major Vedic Mathematics Sutras.

Students can:

1. Browse the Sutras
2. Read explanations
3. View examples
4. Learn step-by-step solving methods
5. Practice questions
6. Track their accuracy

---

# 📝 55-Question Quiz

The application includes a:

```text
55-Question Vedic Mathematics Challenge
```

Quiz features include:

* Multiple-choice questions
* Live progress tracking
* Automatic answer saving
* Refresh-safe progress
* Correct/wrong answer tracking
* Progress percentage
* Quiz attempt tracking

When a student answers a question, the answer can be saved to the database so the student can continue later.

---

# 📊 Dashboard

The dashboard provides an overview of the student's learning progress.

It can display:

* Total practice questions
* Correct answers
* Wrong answers
* Accuracy percentage
* Sutras attempted
* Sutras mastered
* Quiz progress
* Current learning streak

---

# 👤 Profile

The profile page combines statistics from:

```text
Practice + Quiz
```

Students can:

* View their name
* View email
* Upload profile photo
* Edit profile name
* View total questions
* View correct answers
* View accuracy
* View current streak
* View learning progress

---

# 🔥 Daily Learning Streak

The application tracks the student's daily activity.

A streak can be updated when the student submits:

* A quiz answer
* A practice answer

The database uses:

```text
last_active_date
current_streak
```

to track the student's learning streak.

---

# 🏆 Sutra Mastery

A Sutra is considered **mastered** when the student satisfies the configured mastery requirements.

The default configuration is:

```python
MASTERY_THRESHOLD = 80
MIN_ATTEMPTS_FOR_MASTERY = 5
```

This means a student needs:

```text
Minimum 5 attempts
+
80% or higher accuracy
```

to have a Sutra counted as mastered.

These values can be changed in `app.py`.

---

# 🤖 AI Scan

The project includes an AI Scan page as a placeholder for future development.

The planned functionality can include:

* Uploading a mathematical problem
* Image recognition
* Mathematical problem detection
* Step-by-step solution generation
* Vedic Mathematics technique suggestions

The project includes the Google Generative AI package:

```bash
pip install google-generativeai
```

For production use, configure the required API key through environment variables.

---

# ⚡ Speed Test

The Speed Test page is intended to help students measure their calculation speed.

Possible future features include:

* Timed questions
* Questions per minute
* Average solving time
* Accuracy percentage
* Difficulty levels
* Personal best score
* Speed comparison

---

# 🖼️ Pillow

Pillow is installed for image-related functionality such as profile photo processing.

Install it using:

```bash
pip install Pillow
```

It can be used for:

* Image validation
* Image resizing
* Image processing
* Profile photo handling

---

# 🔧 Common Issues

## 1. `1054 Unknown column`

### Cause

The database table is missing a column expected by the Flask application.

### Solution

Check the table structure:

```sql
DESCRIBE students;
```

or:

```sql
DESCRIBE quiz_attempts;
```

Make sure all required columns exist.

---

# 2. `No database selected`

### Cause

MySQL has not selected the `vedic_math` database.

### Solution

Run:

```sql
USE vedic_math;
```

Or select:

```text
vedic_math
```

from the MySQL Workbench schema panel.

---

# 3. `1452 Foreign Key Constraint Fails`

Example:

```text
Cannot add or update a child row:
a foreign key constraint fails
```

### Cause

The referenced record does not exist.

For example, if the application tries to create a quiz attempt using:

```text
quiz_id = 1
```

but quiz ID 1 does not exist.

### Solution

Check:

```sql
SELECT * FROM quizzes;
```

If the quiz is missing:

```sql
INSERT INTO quizzes (id, title)
VALUES (1, 'Vedic Mathematics Challenge');
```

---

# 4. `BuildError: Could not build url for endpoint`

### Cause

A Flask route is:

* Missing
* Misspelled
* Incorrectly named
* Incorrectly referenced in a template

### Solution

Check:

```python
@app.route(...)
```

and compare the endpoint name with:

```python
url_for(...)
```

---

# 5. `ERR_CONNECTION_RESET`

### Cause

The Flask server may have crashed.

### Solution

Check the terminal for the Python traceback.

Then restart:

```bash
python app.py
```

---

# 6. MySQL Access Denied

Example:

```text
Access denied for user 'root'
```

### Cause

The MySQL username or password is incorrect.

### Solution

Check your:

```python
DB_CONFIG
```

Example:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "vedic_math"
}
```

---

# 7. `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'flask'
```

Install the required dependency:

```bash
pip install flask
```

For all dependencies:

```bash
pip install flask mysql-connector-python werkzeug python-dotenv google-generativeai Pillow
```

---

# 8. Profile Image Not Uploading

Make sure the upload directory exists:

```text
static/uploads/
```

If it doesn't exist, create it:

```bash
mkdir static/uploads
```

Also make sure the Flask application has permission to write to the directory.

---

# 📦 Requirements File

It is recommended to create a:

```text
requirements.txt
```

file.

Example:

```text
Flask
mysql-connector-python
Werkzeug
python-dotenv
google-generativeai
Pillow
```

Then all dependencies can be installed using:

```bash
pip install -r requirements.txt
```

---

# 🔄 Recommended Installation Workflow

For a fresh installation, the easiest process is:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Vedic-Maths

python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the database:

```sql
CREATE DATABASE vedic_math;
USE vedic_math;
```

Run all required table creation queries.

Configure `app.py` or `.env`.

Finally:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🔒 Security Notes

For development, a local MySQL configuration may look like:

```python
"password": ""
```

However, for production:

* Never hard-code database passwords
* Never hard-code API keys
* Use environment variables
* Keep `.env` out of Git
* Use strong Flask secret keys
* Validate uploaded files
* Restrict upload file types
* Use HTTPS in production

Example `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
static/uploads/*
```

---

# 🧪 Testing the Application

After starting the application, test the following flow:

### 1. Registration

Open:

```text
/register
```

Create a new account.

### 2. Login

Open:

```text
/login
```

Log in using the newly created account.

### 3. Dashboard

Open:

```text
/dashboard
```

Verify that the dashboard displays the logged-in student's information.

### 4. Sutras

Open:

```text
/sutras
```

Verify that all 16 Sutras are displayed.

### 5. Practice

Select a Sutra and answer practice questions.

Verify that practice answers are saved.

### 6. Quiz

Open:

```text
/quiz
```

Answer questions and refresh the page.

Verify that the saved progress is restored.

### 7. Profile

Open:

```text
/profile
```

Verify:

* Student information
* Practice statistics
* Quiz statistics
* Accuracy
* Streak
* Profile photo

---

# 📈 Future Development

Possible future improvements:

* 🤖 Fully functional AI Math Scanner
* ⚡ Advanced Speed Test
* 🏆 Leaderboard
* 🥇 Student achievements and badges
* 📊 Advanced performance analytics
* 📚 More practice questions
* 🎯 Difficulty-based questions
* 🔔 Learning reminders
* 📱 Fully responsive mobile application
* 🌐 Deploy application to AWS
* 🔐 Improved authentication
* 🧪 Automated testing
* 🐳 Docker support
* ⚙️ CI/CD pipeline using Jenkins
* ☁️ Cloud database integration

---

# 👨‍💻 Development Notes

Quiz correctness is currently handled on the client side in:

```text
quiz.js
```

because the quiz questions are stored in JavaScript rather than in the database.

This is acceptable for learning/demo purposes, but it is **not tamper-proof**.

For a production application, questions and correct answers should ideally be stored and validated on the server side.

---

# 📌 Project Summary

**Vedic Mathematics Learning Platform** provides an interactive environment for students to learn and practice Vedic Mathematics.

The platform combines:

```text
Learning
   ↓
Practice
   ↓
Quiz
   ↓
Performance Tracking
   ↓
Streaks
   ↓
Sutra Mastery
```

The application uses:

```text
Frontend
HTML + CSS + Bootstrap + JavaScript

Backend
Python + Flask

Database
MySQL

Additional Libraries
python-dotenv
Google Generative AI
Pillow
```

---

# 📄 License

This project is developed for educational and learning purposes.

You may modify and improve the project according to your requirements.

---

# 🙏 Acknowledgement

This project was developed as an educational project to demonstrate:

* Python Flask development
* MySQL database integration
* User authentication
* CRUD operations
* Quiz management
* Progress tracking
* Practice analytics
* File uploads
* JavaScript interaction
* AI integration concepts
* Web application development
