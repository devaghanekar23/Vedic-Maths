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

-- Quiz Results

USE vedic_math;

CREATE TABLE IF NOT EXISTS quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    score INT NOT NULL DEFAULT 0,

    total_questions INT NOT NULL DEFAULT 0,

    percentage DECIMAL(5,2) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_quiz_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);
