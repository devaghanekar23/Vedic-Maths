# Vedic Mathematics Learning Platform

A Flask + MySQL web application to learn and practice the 16 Vedic Math Sutras, take a 55-question quiz, track practice accuracy, and monitor daily learning streaks.

---

## Features

- User registration & login
- Dashboard with practice stats (accuracy, sutras attempted/mastered)
- 16 Vedic Sutras with step-by-step solvers and live practice questions
- 55-question multiple choice quiz with live progress saving (auto-saves as you answer, refresh-safe)
- Profile page with combined stats from Quiz + Practice, and a day streak counter
- Editable profile (name + photo upload)
- AI Scan and Speed Test placeholder pages

---

## Tech Stack

- **Backend:** Python (Flask)
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap 5, vanilla JavaScript
- **DB Driver:** `mysql-connector-python`

---

## Prerequisites

Before running this project, make sure you have:

1. **Python 3.10+** installed — [python.org](https://www.python.org/downloads/)
2. **MySQL Server** running locally (e.g. via XAMPP, WAMP, or MySQL directly) — and **MySQL Workbench** or phpMyAdmin to run SQL scripts
3. **pip** (comes with Python)

---

## Step 1 — Get the project files

Copy/clone the project folder onto your machine. The folder structure should look roughly like this:

```
Vedic-Maths/
├── app.py
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/        (auto-created for profile photos)
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── profile.html
    ├── quiz.html
    ├── practice.html
    ├── practice_details.html
    ├── sutras.html
    ├── sutra_detail.html
    ├── ai_scan.html
    ├── speed_test.html
    ├── contact.html
    └── 404.html
```

---

## Step 2 — Install Python dependencies

Open a terminal in the project folder and run:

```bash
pip install flask mysql-connector-python werkzeug
```

(If you use a virtual environment, activate it first before running this command.)

---

## Step 3 — Set up the MySQL database

1. Open MySQL Workbench (or phpMyAdmin) and create a new database:

```sql
CREATE DATABASE vedic_math;
USE vedic_math;
```

2. Run the following table creation scripts **in this order**:

### `students` table
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

### `quizzes` table
```sql
CREATE TABLE quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    total_questions INT DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert the default quiz (id = 1) used by app.py
INSERT INTO quizzes (id, title) VALUES (1, 'Vedic Mathematics Challenge');
```

### `quiz_attempts` table
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

    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);
```

### `student_answers` table (per-question quiz tracking)
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

    UNIQUE KEY unique_student_quiz_question (student_id, quiz_id, question_index),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
```

### `practice_answers` table (per-question practice tracking)
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

    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
```

> **Note:** An older table called `practice_results` may also exist from earlier development — it is no longer used by the app and can be ignored or dropped.

---

## Step 4 — Configure the database connection

Open `app.py` and check the `DB_CONFIG` section near the top:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vedic_math"
}
```

Update `user` / `password` if your MySQL setup uses different credentials.

---

## Step 5 — Run the application

From the project folder, run:

```bash
python app.py
```

You should see output like:

```
 * Running on http://127.0.0.1:5000
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## Step 6 — Using the app

1. Register a new account on `/register`
2. Log in on `/login`
3. Explore:
   - `/dashboard` — your learning overview
   - `/sutras` — browse all 16 Vedic Sutras
   - `/practice/<id>` — practice questions for a specific sutra
   - `/quiz` — take the 55-question quiz
   - `/profile` — view combined stats and edit your profile

---

## Common Issues

| Problem | Likely Cause | Fix |
|---|---|---|
| `1054 Unknown column` error | A table is missing a column the code expects | Re-check you ran all `ALTER TABLE` / `CREATE TABLE` scripts in Step 3 |
| `No database selected` in Workbench | Database not set as active | Double-click `vedic_math` in the SCHEMAS sidebar, or run `USE vedic_math;` first |
| `1452 foreign key constraint fails` | Referenced row doesn't exist yet (e.g. quiz_id = 1 missing from `quizzes`) | Make sure the `INSERT INTO quizzes...` line in Step 3 was run |
| `BuildError: Could not build url for endpoint` | A Flask route is missing/misspelled/misplaced | Check `app.py` for correct `@app.route` indentation and route names |
| `ERR_CONNECTION_RESET` in browser | Flask server crashed or isn't running | Check the terminal for a Python traceback and re-run `python app.py` |

---

## Notes for Future Development

- Quiz correctness is currently checked **client-side** (in `quiz.js`), since quiz questions live in the JS file rather than the database. This is fine for casual use but not tamper-proof.
- "Sutras Mastered" counts a sutra as mastered once a student has attempted at least 5 questions on it with 80%+ accuracy (adjustable via `MASTERY_THRESHOLD` and `MIN_ATTEMPTS_FOR_MASTERY` in `app.py`).
- Day streak updates automatically whenever a student submits a quiz answer or a practice answer.
