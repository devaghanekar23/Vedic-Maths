CREATE DATABASE vedic_math;

USE vedic_math;


CREATE TABLE students(

id INT AUTO_INCREMENT PRIMARY KEY,

name VARCHAR(100) NOT NULL,

email VARCHAR(100) UNIQUE NOT NULL,

password VARCHAR(255) NOT NULL,

profile_pic VARCHAR(255) DEFAULT 'default.png',

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



USE vedic_math;

-- ============================================================
-- PRACTICE RESULTS
-- ============================================================

CREATE TABLE IF NOT EXISTS practice_results (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    sutra_id INT NOT NULL,

    question_id INT NOT NULL,

    user_answer VARCHAR(255),

    correct_answer VARCHAR(255),

    is_correct TINYINT(1) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_practice_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);

-- Quiz table

CREATE TABLE quizzes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    total_questions INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- questions table

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_number INT NOT NULL,
    question_text TEXT NOT NULL,
    correct_option CHAR(1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (quiz_id)
        REFERENCES quizzes(id)
        ON DELETE CASCADE
);

-- Question Option Table
CREATE TABLE question_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_label CHAR(1) NOT NULL,
    option_text VARCHAR(500) NOT NULL,

    FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE
);

-- quiz_attempts table

CREATE TABLE quiz_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
    quiz_id INT NOT NULL,

    current_question INT DEFAULT 1,

    total_questions INT DEFAULT 0,
    attempted_questions INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    wrong_answers INT DEFAULT 0,

    progress_percentage DECIMAL(5,2) DEFAULT 0.00,

    status ENUM('not_started', 'in_progress', 'completed')
        DEFAULT 'not_started',

    started_at TIMESTAMP NULL,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    completed_at TIMESTAMP NULL,

    FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    FOREIGN KEY (quiz_id)
        REFERENCES quizzes(id)
        ON DELETE CASCADE,

    UNIQUE KEY unique_student_quiz (student_id, quiz_id)
);

-- Quize Answer Table

CREATE TABLE quiz_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,

    attempt_id INT NOT NULL,
    question_id INT NOT NULL,

    selected_option CHAR(1) NULL,
    correct_option CHAR(1) NOT NULL,

    is_correct BOOLEAN DEFAULT FALSE,

    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (attempt_id)
        REFERENCES quiz_attempts(id)
        ON DELETE CASCADE,

    FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE,

    UNIQUE KEY unique_attempt_question (attempt_id, question_id)
);

CREATE TABLE IF NOT EXISTS student_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    quiz_id INT NOT NULL,
    question_index INT NOT NULL,          -- 0-based index (questions array ka index)
    selected_option VARCHAR(255) NOT NULL,
    is_correct TINYINT(1) NOT NULL DEFAULT 0,
    answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_student_quiz_question (student_id, quiz_id, question_index),

    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS practice_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    sutra_id INT NOT NULL,
    question_id INT NOT NULL,
    user_answer VARCHAR(255),
    correct_answer VARCHAR(255),
    is_correct TINYINT(1) NOT NULL DEFAULT 0,
    answered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
);