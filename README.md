# 🧮 Vedic Mathematics Learning Platform

A Flask + MySQL based web application for learning and practicing **Vedic Mathematics**.

The platform allows students to learn the **16 Vedic Math Sutras**, practice questions, take quizzes, track accuracy and progress, maintain daily streaks, use AI-powered maths assistance, update their profile, view the leaderboard, and unlock achievement certificates.

---

## 📌 Features

### 👤 User Management

* User registration
* User login/logout
* Google Login
* Session-based authentication
* Individual student dashboard
* Individual profile
* Edit profile information
* Upload profile picture

### 📚 Vedic Mathematics

* Learn all **16 Vedic Sutras**
* Sanskrit name and meaning
* Explanation of each Sutra
* Formula/rule
* Example questions
* Step-by-step solutions
* Previous/Next Sutra navigation

### ✏️ Practice

* Practice all 16 Sutras
* 20 questions generated for each Sutra
* Automatic answer checking
* Step-by-step solution after submission
* Practice answers stored for each logged-in student
* Accuracy tracking
* Sutra mastery tracking

### 📝 Quiz

* 55-question quiz
* Question progress tracking
* Correct/wrong answer tracking
* Quiz progress saved in the database
* Quiz completion status

### 🤖 AI Maths Assistant

* Enter a mathematical question
* Upload an image of a maths problem
* Use camera input
* AI explains the solution step-by-step
* Vedic Mathematics approach is used where applicable

### 🏆 Progress & Achievements

* Total problems solved
* Accuracy percentage
* Sutras mastered
* Overall progress
* Daily streak
* Leaderboard
* Achievement milestones
* Certificates

---

# 🛠️ Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Backend programming             |
| Flask            | Web framework                   |
| MySQL            | Database                        |
| HTML             | Frontend structure              |
| CSS              | Frontend styling                |
| JavaScript       | Frontend functionality          |
| Google Gemini AI | AI maths assistance             |
| Google OAuth     | Google Login                    |
| Pillow           | Image processing                |
| python-dotenv    | Environment variable management |

The Flask application connects to the `vedic_math` MySQL database and uses session-based `student_id` authentication to load each student's own dashboard and progress.

---

# 📋 Requirements

Before installing the project, make sure the following are installed.

### Required Software

1. Python 3.10 or newer
2. MySQL Server
3. MySQL Workbench — optional
4. Git — optional
5. Google account — required for Google Login
6. Gemini API key — required for AI features

---

# 📁 Project Structure

Your project should have a structure similar to:

```text
Vedic-Maths/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── sutras.html
│   ├── sutra_detail.html
│   ├── practice.html
│   ├── practice_details.html
│   ├── quiz.html
│   ├── ai_scan.html
│   ├── leaderboard.html
│   ├── certificates.html
│   ├── speed_test.html
│   ├── contact.html
│   └── 404.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
└── database/
    └── vedic_math.sql
```

---

# 🚀 Installation Guide

## Step 1 — Clone the Repository

If your project is available on GitHub:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Example:

```bash
git clone https://github.com/yourusername/Vedic-Maths.git
```

Move into the project:

```bash
cd Vedic-Maths
```

If you already have the project folder, simply open the terminal inside the project directory.

---

# Step 2 — Create a Python Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

After activation, you should see something similar to:

```text
(venv) C:\Vedic-Maths>
```

### Linux / Ubuntu / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# Step 3 — Upgrade pip

Run:

```bash
python -m pip install --upgrade pip
```

---

# Step 4 — Install Python Dependencies

Create a file named:

```text
requirements.txt
```

Add:

```text
Flask
mysql-connector-python
Pillow
google-generativeai
python-dotenv
google-auth
google-auth-oauthlib
google-auth-httplib2
Werkzeug
```

Then install everything using:

```bash
pip install -r requirements.txt
```

This is the easiest installation method because all required Python packages are installed with one command.

---

# Step 5 — Verify Python Packages

Run:

```bash
pip list
```

You should see packages including:

```text
Flask
mysql-connector-python
Pillow
google-generativeai
python-dotenv
google-auth
google-auth-oauthlib
google-auth-httplib2
Werkzeug
```

---

# 🗄️ MySQL Database Setup

## Step 6 — Start MySQL

Make sure MySQL Server is running.

### Windows

Open:

```text
Services
```

Find:

```text
MySQL
```

and make sure the service is running.

You can also use MySQL Workbench.

### Ubuntu

```bash
sudo systemctl start mysql
```

Check status:

```bash
sudo systemctl status mysql
```

---

# Step 7 — Create the Database

Open MySQL:

```bash
mysql -u root -p
```

Enter your MySQL password.

Then create the database:

```sql
CREATE DATABASE vedic_math;
```

Select it:

```sql
USE vedic_math;
```

---

# Step 8 — Import the Database

If your project contains:

```text
database/vedic_math.sql
```

you can import it using:

```bash
mysql -u root -p vedic_math < database/vedic_math.sql
```

Or use MySQL Workbench:

```text
File
→ Open SQL Script
→ Select vedic_math.sql
→ Execute
```

---

# 🧑‍🎓 Student Database

The application uses the `students` table for registered users.

The application checks whether an email already exists before registering a new student and then stores the student's name, email and password.

The application also stores the logged-in user's database ID in the Flask session:

```python
session["student_id"] = student["id"]
```

This allows different users to see their own dashboard and progress.

---

# 🔐 Database Configuration

The current application contains this database configuration:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vedic_math"
}
```

The database connection is created using:

```python
mysql.connector.connect(**DB_CONFIG)
```

## Recommended Configuration

For better security, use environment variables instead of putting passwords directly inside `app.py`.

Create:

```text
.env
```

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=vedic_math

GEMINI_API_KEY=your_gemini_api_key

FLASK_SECRET_KEY=your_secret_key
```

Then update your Python application to read these values from `.env`.

---

# 🤖 Gemini AI Setup

The application uses Google's Gemini API for the AI Maths Assistant.

The application loads:

```python
GEMINI_API_KEY
```

from the environment and configures the Gemini model.

## Step 1 — Get Gemini API Key

Create a Gemini API key from Google's Gemini developer platform.

Do **not** put the API key directly into GitHub.

Add it to:

```text
.env
```

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

---

# 🔑 Google Login Setup

The application supports Google Login using Google OAuth.

The application verifies the Google credential and checks whether the email has been verified by Google.

You need to configure a Google OAuth Client ID.

Your application currently contains a Google Client ID configuration.

For production deployment, keep OAuth configuration in environment variables rather than hard-coding credentials.

---

# 📂 Upload Folder

The application automatically creates:

```text
static/uploads/
```

The application supports:

```text
PNG
JPG
JPEG
GIF
WEBP
```

for profile pictures.

If the folder does not exist, the application creates it automatically.

---

# ▶️ Run the Application

Activate your virtual environment first.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Then run:

```bash
python app.py
```

The application runs on:

```text
http://127.0.0.1:5000
```

The current application configuration uses Flask port `5000` and host `127.0.0.1`.

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 🌐 Main Application Pages

| URL              | Purpose              |
| ---------------- | -------------------- |
| `/`              | Home page            |
| `/register`      | Student registration |
| `/login`         | Student login        |
| `/logout`        | Logout               |
| `/dashboard`     | Student dashboard    |
| `/profile`       | Student profile      |
| `/edit-profile`  | Edit profile         |
| `/sutras`        | All 16 Sutras        |
| `/sutra/<id>`    | Individual Sutra     |
| `/practice`      | Practice selection   |
| `/practice/<id>` | Sutra practice       |
| `/quiz`          | 55-question quiz     |
| `/ai-scan`       | AI Maths Assistant   |
| `/leaderboard`   | Student leaderboard  |
| `/certificates`  | Achievements         |
| `/speed-test`    | Speed test           |
| `/contact`       | Contact page         |

---

# 👤 How a New User Uses the Application

## 1. Open the Website

Go to:

```text
http://127.0.0.1:5000
```

---

## 2. Register

Click:

```text
Register
```

Enter:

```text
Name
Email
Password
```

Then click:

```text
Register
```

The user will be stored in the MySQL `students` table.

---

## 3. Login

After registration:

```text
Login
```

Enter:

```text
Email
Password
```

The application verifies the credentials.

After successful login, the user's unique database ID is stored in the session.

---

# 📊 Dashboard

After login, the user is redirected to:

```text
/dashboard
```

The dashboard displays information for the currently logged-in student.

The application retrieves the student using:

```sql
SELECT id, name, email, profile_pic
FROM students
WHERE id = %s
```

This prevents one user's dashboard information from being displayed to another user.

---

# 📚 Learn Vedic Sutras

Go to:

```text
Sutras
```

The application contains:

```text
1. Ekadhikena Purvena
2. Nikhilam Navatashcaramam Dashatah
3. Urdhva Tiryagbhyam
4. Paravartya Yojayet
5. Shunyam Saamyasamuccaye
6. Anurupyena
7. Sankalana Vyavakalanabhyam
8. Puranapuranabhyam
9. Chalana Kalanabhyam
10. Yavadunam
11. Vyastisamanstih
12. Shesanyankena Charamena
13. Sopantyadvayamantyam
14. Ekanyunena Purvena
15. Gunitasamuccayah
16. Gunakasamuccayah
```

Each Sutra has an explanation, rule and example.

---

# ✏️ Practice

Go to:

```text
/practice
```

Select any Sutra.

The application generates:

```text
20 Questions
```

for each Sutra.

When a student submits an answer:

1. The answer is checked.
2. The correct answer is calculated.
3. Step-by-step solution is displayed.
4. The result is stored against the logged-in student's ID.
5. The student's streak can be updated.

Practice answers are saved using the current session's `student_id`.

---

# 📝 Quiz

Go to:

```text
/quiz
```

The application provides a:

```text
55-question quiz
```

Quiz progress includes:

```text
Total Questions
Attempted Questions
Correct Answers
Wrong Answers
Progress Percentage
Current Question
Status
```

The quiz stores progress against the logged-in student's ID.

---

# 🤖 AI Maths Assistant

Go to:

```text
/ai-scan
```

You can provide:

```text
Mathematical question
```

or:

```text
Image of a mathematical problem
```

The application can also process camera image data.

The AI is instructed to solve mathematical problems step-by-step using Vedic Mathematics techniques where applicable.

---

# 🏆 Leaderboard

Go to:

```text
/leaderboard
```

The leaderboard calculates student performance using:

```text
Correct Answers
Total Attempts
Accuracy
Current Streak
```

It can display up to the top 50 students.

---

# 🏅 Certificates & Achievements

Go to:

```text
/certificates
```

Achievement levels include:

| Progress | Achievement          |
| -------: | -------------------- |
|      25% | 🥉 Bronze Achiever   |
|      50% | 🥈 Silver Achiever   |
|      75% | 🥇 Gold Achiever     |
|     100% | 🏆 Vedic Math Master |

The application calculates achievement progress from the number of mastered Sutras.

---

# 👤 Profile

After login, users can open:

```text
/profile
```

The profile can show:

```text
Name
Email
Profile Picture
Problems Solved
Accuracy
Sutras Mastered
Overall Progress
Daily Streak
```

The profile statistics are calculated specifically for the logged-in student's ID.

---

# 🖼️ Edit Profile

Go to:

```text
/edit-profile
```

The user can:

* Change name
* Upload profile picture
* Keep existing profile picture
* Save profile changes

Supported image formats:

```text
PNG
JPG
JPEG
GIF
WEBP
```

The uploaded profile image is associated with the logged-in student's ID.

---

# 🚪 Logout

Click:

```text
Logout
```

or visit:

```text
/logout
```

The application clears the current Flask session and returns the user to the home page.

---

# 🔒 User Data Isolation

Each registered student has a unique:

```text
student_id
```

When a user logs in, the application stores:

```python
session["student_id"] = student["id"]
```

Every protected page uses this ID to retrieve the correct user's data.

For example:

```sql
WHERE id = %s
```

and:

```sql
WHERE student_id = %s
```

are used throughout the application.

This means:

```text
User A
   ↓
student_id = 1
   ↓
Only User A's data

User B
   ↓
student_id = 2
   ↓
Only User B's data
```

This is an important part of the application's multi-user functionality.

---

# ⚠️ Common Errors

## Error 1 — `ModuleNotFoundError`

Example:

```text
ModuleNotFoundError: No module named 'flask'
```

Solution:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install Flask
```

---

## Error 2 — MySQL Connection Error

Example:

```text
mysql.connector.errors.InterfaceError
```

Check:

1. MySQL is running.
2. Database name is correct.
3. Username is correct.
4. Password is correct.
5. MySQL is running on the expected host/port.

Check database:

```sql
SHOW DATABASES;
```

You should see:

```text
vedic_math
```

---

# ❌ Error 3 — `Unknown database 'vedic_math'`

Create the database:

```sql
CREATE DATABASE vedic_math;
```

Then import your SQL file.

---

# ❌ Error 4 — `Access denied for user 'root'`

Check your MySQL username and password.

Test:

```bash
mysql -u root -p
```

If MySQL asks for a password, enter the correct password.

Then update your `.env`:

```env
DB_USER=root
DB_PASSWORD=your_password
```

---

# ❌ Error 5 — Gemini API Error

Check that:

```text
GEMINI_API_KEY
```

exists in your `.env`.

Example:

```env
GEMINI_API_KEY=your_api_key
```

Restart the application after changing `.env`.

---

# ❌ Error 6 — Google Login Not Working

Check:

* Google Client ID
* Authorized JavaScript origins
* Authorized redirect/origin configuration
* Google OAuth configuration
* Browser console errors

Also make sure the Google email is verified.

The application explicitly checks Google's `email_verified` value.

---

# ❌ Error 7 — Profile Image Not Uploading

Check:

```text
static/uploads/
```

Make sure the directory exists.

The application creates this directory automatically, but it must be writable by the application process.

Use only:

```text
PNG
JPG
JPEG
GIF
WEBP
```

---

# ❌ Error 8 — User A Sees User B's Data

Make sure the application uses:

```python
session["student_id"]
```

after login.

Do not use hard-coded student information.

Correct approach:

```python
student_id = session["student_id"]
```

Then query:

```sql
WHERE student_id = %s
```

or:

```sql
WHERE id = %s
```

depending on the table.

The current application already follows this session-based pattern on dashboard and profile routes.

---

# 🧪 Test the Application

After starting the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Test the following flow:

```text
Home
 ↓
Register
 ↓
Login
 ↓
Dashboard
 ↓
Sutras
 ↓
Practice
 ↓
Submit Answer
 ↓
Profile
 ↓
Leaderboard
 ↓
Certificates
 ↓
Logout
```

Also test:

```text
Google Login
AI Scan
Profile Image Upload
Quiz
```

---

# 👥 Multi-User Testing

To verify that user data is separated correctly:

### Test User 1

Register:

```text
Name: Rahul
Email: rahul@example.com
Password: 123456
```

Login as Rahul and complete some practice questions.

Logout.

### Test User 2

Register:

```text
Name: Amit
Email: amit@example.com
Password: 123456
```

Login as Amit.

Amit should have his own:

```text
Dashboard
Practice History
Quiz Progress
Accuracy
Streak
Profile
```

Rahul's practice history should not appear in Amit's profile.

---

# 🛑 Before Production Deployment

Do **not** use the development configuration directly for a public website.

The current application runs Flask with:

```python
debug=True
host="127.0.0.1"
port=5000
```

For production:

* Set `DEBUG=False`
* Use a strong Flask secret key
* Store secrets in environment variables
* Never commit `.env`
* Use hashed passwords
* Use HTTPS
* Configure a production WSGI server such as Gunicorn
* Use a production MySQL user instead of root
* Restrict database access
* Configure Google OAuth production URLs
* Protect uploaded files
* Configure proper logging

---

# 🔐 `.gitignore`

Create:

```text
.gitignore
```

Add:

```text
venv/
.env
__pycache__/
*.pyc
static/uploads/*
```

Do not upload:

```text
.env
```

to GitHub.

---

# 📦 Complete Installation — Quick Version

For a new computer, the basic commands are:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Vedic-Maths

python -m venv venv

venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# 🐧 Ubuntu Installation

Install Python:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Install MySQL:

```bash
sudo apt install mysql-server
```

Start MySQL:

```bash
sudo systemctl start mysql
```

Clone project:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Vedic-Maths
```

Create environment:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

---

# 🪟 Windows Installation

Install:

```text
Python
MySQL
Git
```

Then:

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd Vedic-Maths
```

Create virtual environment:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 📌 Important Notes

### Database

The application expects:

```text
Database: vedic_math
```

### Python

Use a virtual environment:

```bash
python -m venv venv
```

### Dependencies

Install:

```bash
pip install -r requirements.txt
```

### Application

Run:

```bash
python app.py
```

### Website

Open:

```text
http://127.0.0.1:5000
```

### AI

Configure:

```text
GEMINI_API_KEY
```

### Google Login

Configure your Google OAuth Client ID and allowed origins.

---

# 🎯 User Journey

```text
                    VEDIC MATHS
                         │
                         ▼
                       HOME
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          REGISTER                 LOGIN
              │                     │
              └──────────┬──────────┘
                         ▼
                     DASHBOARD
                         │
       ┌─────────┬───────┼────────┬──────────┐
       ▼         ▼       ▼        ▼          ▼
     SUTRAS   PRACTICE  QUIZ    AI SCAN   PROFILE
       │         │       │        │          │
       └─────────┴───────┴────────┴──────────┘
                         │
                         ▼
                  PROGRESS TRACKING
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
         LEADERBOARD           CERTIFICATES
```

---

# ❤️ Project Purpose

The goal of this application is to make **Vedic Mathematics easy, interactive and accessible** for students.

Students can:

* Learn
* Practice
* Solve
* Get instant explanations
* Track their progress
* Compete on the leaderboard
* Earn achievements

all from one platform.

---

# 👨‍💻 Developer

**Vedic Mathematics Learning Platform**

Built using:

```text
Python
Flask
MySQL
HTML
CSS
JavaScript
Google Gemini AI
Google OAuth
```

---

# 📄 License

This project can be used for educational and learning purposes.

---

# ⭐ Final Setup Checklist

Before sharing the application with users, verify:

* [ ] Python installed
* [ ] MySQL installed
* [ ] MySQL service running
* [ ] `vedic_math` database created
* [ ] Database tables imported
* [ ] Virtual environment created
* [ ] Virtual environment activated
* [ ] `requirements.txt` installed
* [ ] `.env` configured
* [ ] Gemini API key configured
* [ ] Google Login configured
* [ ] `static/uploads/` available
* [ ] Application starts without errors
* [ ] Registration works
* [ ] Login works
* [ ] Logout works
* [ ] Dashboard works
* [ ] Practice works
* [ ] Quiz works
* [ ] AI Scan works
* [ ] Profile works
* [ ] Leaderboard works
* [ ] Certificates work
* [ ] Multiple users see separate data

---

## 🚀 Start the Application

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Flask application
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

**Your Vedic Mathematics Learning Platform is ready to use! 🎉**
