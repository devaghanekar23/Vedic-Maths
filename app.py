import os
import random
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import make_response

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
app.secret_key = "vedic-maths-secret-key-2026"


# ============================================================
# TEMP STUDENT DATABASE
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "vedic_math"
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ============================================================
# 16 VEDIC SUTRAS
# ============================================================

sutras_list = [
    {
        "id": 1,
        "icon": "⚡",
        "name": "Ekadhikena Purvena",
        "sanskrit": "एकाधिकेन पूर्वेण",
        "meaning": "By one more than the previous one.",
        "introduction": "Used here for finding squares of numbers ending in 5.",
        "rule": "Multiply the number before 5 by the next number and attach 25.",
        "example_question": "25²",
        "example_answer": "625",
        "operation": "square",
    },
    {
        "id": 2,
        "icon": "🔷",
        "name": "Nikhilam Navatashcaramam Dashatah",
        "sanskrit": "निखिलं नवतश्चरमं दशतः",
        "meaning": "All from 9 and the last from 10.",
        "introduction": "Used mainly for multiplication of numbers close to a convenient base such as 10, 100 or 1000.",
        "rule": "Find deviations from the base, perform the cross operation and multiply the deviations.",
        "example_question": "98 × 97",
        "example_answer": "9506",
        "operation": "multiplication",
    },
    {
        "id": 3,
        "icon": "📐",
        "name": "Urdhva Tiryagbhyam",
        "sanskrit": "ऊर्ध्वतिर्यग्भ्याम्",
        "meaning": "Vertically and Crosswise.",
        "introduction": "A general multiplication technique using vertical and crosswise multiplication.",
        "rule": "Multiply vertically and crosswise, keeping track of carries.",
        "example_question": "23 × 14",
        "example_answer": "322",
        "operation": "multiplication",
    },
    {
        "id": 4,
        "icon": "🎯",
        "name": "Paravartya Yojayet",
        "sanskrit": "परावर्त्य योजयेत्",
        "meaning": "Transpose and Apply.",
        "introduction": "Used here for simple exact division problems.",
        "rule": "Use the divisor and quotient relationship to obtain and verify the answer.",
        "example_question": "20 ÷ 5",
        "example_answer": "4",
        "operation": "division",
    },
    {
        "id": 5,
        "icon": "📊",
        "name": "Shunyam Saamyasamuccaye",
        "sanskrit": "शून्यं साम्यसमुच्चये",
        "meaning": "When the sum is equal, that sum is zero.",
        "introduction": "Used here to demonstrate a simple equation-solving pattern.",
        "rule": "Move the known constant to the opposite side and calculate the unknown.",
        "example_question": "x + 5 = 9",
        "example_answer": "x = 4",
        "operation": "algebra",
    },
    {
        "id": 6,
        "icon": "➕",
        "name": "Anurupyena",
        "sanskrit": "अनुरूप्येण",
        "meaning": "Proportionately.",
        "introduction": "Uses a convenient working base or proportional relationship.",
        "rule": "Choose a convenient working base and calculate using deviations.",
        "example_question": "48 × 46",
        "example_answer": "2208",
        "operation": "multiplication",
    },
    {
        "id": 7,
        "icon": "🧩",
        "name": "Sankalana Vyavakalanabhyam",
        "sanskrit": "संकलनव्यवकलनाभ्याम्",
        "meaning": "By Addition and Subtraction.",
        "introduction": "Uses addition and subtraction together to obtain useful relationships.",
        "rule": "Calculate the required sum and difference.",
        "example_question": "10 + 5",
        "example_answer": "15",
        "operation": "addition",
    },
    {
        "id": 8,
        "icon": "🔶",
        "name": "Puranapuranabhyam",
        "sanskrit": "पूरणापूरणाभ्याम्",
        "meaning": "By Completion and Non-Completion.",
        "introduction": "Uses completion to a convenient number and then adjusts the remaining value.",
        "rule": "Complete a number to a convenient multiple of 10 and add the remaining amount.",
        "example_question": "99 + 48",
        "example_answer": "147",
        "operation": "completion",
    },
    {
        "id": 9,
        "icon": "📈",
        "name": "Chalana Kalanabhyam",
        "sanskrit": "चलनकलनाभ्याम्",
        "meaning": "Differences and Similarities.",
        "introduction": "Used here to demonstrate calculation through differences.",
        "rule": "Find the difference between the given values.",
        "example_question": "|50 - 20|",
        "example_answer": "30",
        "operation": "difference",
    },
    {
        "id": 10,
        "icon": "🟢",
        "name": "Yavadunam",
        "sanskrit": "यावदूनम्",
        "meaning": "Whatever the Deficiency.",
        "introduction": "Used for squaring numbers close to a base such as 100.",
        "rule": "Find the deficiency from the base and use it to obtain the square.",
        "example_question": "97²",
        "example_answer": "9409",
        "operation": "square",
    },
    {
        "id": 11,
        "icon": "🧮",
        "name": "Vyastisamanstih",
        "sanskrit": "व्यष्टिसमष्टिः",
        "meaning": "Part and Whole.",
        "introduction": "Break a calculation into smaller parts and combine the results.",
        "rule": "Split a number into convenient parts and add the partial products.",
        "example_question": "36 × 12",
        "example_answer": "432",
        "operation": "multiplication",
    },
    {
        "id": 12,
        "icon": "🔢",
        "name": "Shesanyankena Charamena",
        "sanskrit": "शेषाण्यङ्केन चरमेण",
        "meaning": "Remainders by the Last Digit.",
        "introduction": "Used here for remainder calculation.",
        "rule": "Find the quotient, multiply by the divisor and subtract from the dividend.",
        "example_question": "123 ÷ 9",
        "example_answer": "R = 6",
        "operation": "remainder",
    },
    {
        "id": 13,
        "icon": "📏",
        "name": "Sopantyadvayamantyam",
        "sanskrit": "सोपान्त्यद्वयमन्त्यम्",
        "meaning": "Ultimate and Twice the Penultimate.",
        "introduction": "Used here to demonstrate the last and twice the previous quantity.",
        "rule": "Take the first value and add twice the second value.",
        "example_question": "10 + 2(5)",
        "example_answer": "20",
        "operation": "algebra",
    },
    {
        "id": 14,
        "icon": "🌟",
        "name": "Ekanyunena Purvena",
        "sanskrit": "एकन्यूनेन पूर्वेण",
        "meaning": "By one less than the previous one.",
        "introduction": "Useful for multiplication by numbers such as 99.",
        "rule": "Take one less than the number and find its complement from 100.",
        "example_question": "25 × 99",
        "example_answer": "2475",
        "operation": "multiplication",
    },
    {
        "id": 15,
        "icon": "✖️",
        "name": "Gunitasamuccayah",
        "sanskrit": "गुणितसमुच्चयः",
        "meaning": "Product of Sum.",
        "introduction": "Used here as a verification technique using digit sums.",
        "rule": "Compare the digit-sum relationship of the factors and product.",
        "example_question": "12 × 3",
        "example_answer": "36",
        "operation": "verification",
    },
    {
        "id": 16,
        "icon": "🏁",
        "name": "Gunakasamuccayah",
        "sanskrit": "गुणकसमुच्चयः",
        "meaning": "Factors of the Sum.",
        "introduction": "Used here to demonstrate factorisation of a quadratic expression.",
        "rule": "Find two numbers whose sum is the middle coefficient and whose product is the constant.",
        "example_question": "(x + 2)(x + 3)",
        "example_answer": "x² + 5x + 6",
        "operation": "factorization",
    },
]

# ============================================================
# GENERATE 20 PRACTICE QUESTIONS
# ============================================================

def generate_20_questions(sutra_id):
    questions = []
    random.seed(sutra_id * 100)

    for i in range(1, 21):
        if sutra_id == 1:
            num1 = random.choice([15, 25, 35, 45, 55, 65, 75, 85, 95])
            num2 = 0
            q_text = f"{num1}²"
        elif sutra_id == 2:
            num1 = random.randint(88, 99)
            num2 = random.randint(88, 99)
            q_text = f"{num1} × {num2}"
        elif sutra_id == 3:
            num1 = random.randint(11, 49)
            num2 = random.randint(11, 49)
            q_text = f"{num1} × {num2}"
        elif sutra_id == 4:
            num2 = random.randint(2, 9)
            num1 = num2 * random.randint(5, 20)
            q_text = f"{num1} ÷ {num2}"
        elif sutra_id == 5:
            num2 = random.randint(2, 9)
            num1 = random.randint(num2 + 1, 20)
            q_text = f"x + {num2} = {num1}"
        elif sutra_id == 6:
            num1 = random.randint(41, 59)
            num2 = random.randint(41, 59)
            q_text = f"{num1} × {num2}"
        elif sutra_id == 7:
            num1 = random.randint(10, 50)
            num2 = random.randint(2, 20)
            q_text = f"{num1} + {num2}"
        elif sutra_id == 8:
            num1 = random.randint(50, 99)
            num2 = random.randint(10, 49)
            q_text = f"{num1} + {num2}"
        elif sutra_id == 9:
            num1 = random.randint(20, 80)
            num2 = random.randint(5, 40)
            q_text = f"|{num1} - {num2}|"
        elif sutra_id == 10:
            num1 = random.randint(91, 99)
            num2 = 0
            q_text = f"{num1}²"
        elif sutra_id == 11:
            num1 = random.randint(10, 50)
            num2 = random.randint(2, 20)
            q_text = f"{num1} × {num2}"
        elif sutra_id == 12:
            num1 = random.randint(20, 150)
            num2 = random.randint(2, 9)
            q_text = f"{num1} ÷ {num2}"
        elif sutra_id == 13:
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 10)
            q_text = f"{num1} + 2({num2})"
        elif sutra_id == 14:
            num1 = random.randint(12, 98)
            num2 = 99
            q_text = f"{num1} × 99"
        elif sutra_id == 15:
            num1 = random.randint(10, 50)
            num2 = random.randint(2, 10)
            q_text = f"{num1} × {num2}"
        else:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            q_text = f"(x + {num1})(x + {num2})"

        questions.append({
            "id": i,
            "num1": num1,
            "num2": num2,
            "q_text": q_text,
        })

    return questions

# ============================================================
# ENGLISH STEP-BY-STEP SOLVERS FOR ALL 16 SUTRAS
# ============================================================

def solve_sutra_1(num1, num2=0):
    n = num1 // 10
    next_num = n + 1
    left = n * next_num
    answer = num1 * num1
    
    steps = [
        "Step 1: The last digit is 5, so the end of the answer will be 25.",
        f"Step 2: Multiply the first digit ({n}) by its next consecutive integer ({next_num}) -> {n} × {next_num} = {left}",
        f"Step 3: Combine both parts together -> {left}25",
        f"Correct Answer = {answer}"
    ]
    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_2(num1, num2):
    dev1 = num1 - 100
    dev2 = num2 - 100
    cross = num1 + dev2
    prod = dev1 * dev2
    answer = num1 * num2

    steps = [
        f"Step 1: Calculate deficiency from base 100: {num1} is ({dev1}) and {num2} is ({dev2})",
        f"Step 2: Perform cross-subtraction -> {num1} - {abs(dev2)} = {cross}",
        f"Step 3: Multiply the deficiencies -> {abs(dev1)} × {abs(dev2)} = {prod:02d}",
        f"Correct Answer = {answer}"
    ]
    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_3(num1, num2):
    answer = num1 * num2
    steps = [
        f"Question: {num1} × {num2}",
        "Step 1: Multiply vertically at the units place.",
        "Step 2: Crosswise multiply and add the products.",
        "Step 3: Vertically multiply at the tens place and add carries.",
        f"Correct Answer = {answer}"
    ]
    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_4(num1, num2):
    if num2 == 0:
        return {"success": False, "message": "Division by zero is not allowed."}
    q, r = num1 // num2, num1 % num2
    res = str(q) if r == 0 else f"{q}"
    steps = [
        f"Question: {num1} ÷ {num2}",
        f"Step 1: Identify divisor ({num2}) and dividend ({num1})",
        f"Step 2: Calculate quotient = {q}" + (f" (Remainder = {r})" if r else ""),
        f"Correct Answer = {res}"
    ]
    return {"success": True, "result": res, "steps": steps}

def solve_sutra_5(num1, num2):
    ans = num1 - num2
    steps = [
        f"Equation: x + {num2} = {num1}",
        f"Step 1: Transpose constant to the right side -> x = {num1} - {num2}",
        f"Correct Answer = x = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_6(num1, num2):
    answer = num1 * num2
    steps = [
        f"Question: {num1} × {num2}",
        "Step 1: Take working base as 50 (Half of 100).",
        "Step 2: Multiply proportionately using working base deviations.",
        f"Correct Answer = {answer}"
    ]
    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_7(num1, num2):
    ans = num1 + num2
    steps = [
        f"Question: {num1} + {num2}",
        "Step 1: Add both numbers directly.",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_8(num1, num2):
    ans = num1 + num2
    steps = [
        f"Question: {num1} + {num2}",
        "Step 1: Complete nearby base first.",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_9(num1, num2):
    ans = abs(num1 - num2)
    steps = [
        f"Question: |{num1} - {num2}|",
        "Step 1: Calculate the absolute difference.",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_10(num1, num2=0):
    dev = 100 - num1
    ans = num1 * num1
    steps = [
        f"Question: {num1}²",
        f"Step 1: Find deficiency from base 100 -> {dev}",
        f"Step 2: Subtract deficiency -> {num1} - {dev} = {num1 - dev}",
        f"Step 3: Square the deficiency -> {dev}² = {dev*dev}",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_11(num1, num2):
    ans = num1 * num2
    steps = [
        f"Question: {num1} × {num2}",
        "Step 1: Split into smaller parts and multiply.",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_12(num1, num2):
    if num2 == 0:
        return {"success": False, "message": "Division by zero."}
    r = num1 % num2
    steps = [
        f"Question: Remainder of {num1} ÷ {num2}",
        "Step 1: Calculate the remainder.",
        f"Correct Answer = Remainder {r}"
    ]
    return {"success": True, "result": str(r), "steps": steps}

def solve_sutra_13(num1, num2):
    ans = num1 + (2 * num2)
    steps = [
        f"Question: {num1} + 2({num2})",
        f"Step 1: Double the penultimate term -> 2 × {num2} = {2*num2}",
        f"Step 2: Add ultimate term -> {num1} + {2*num2} = {ans}",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_14(num1, num2=99):
    ans = num1 * 99
    left = num1 - 1
    right = 100 - num1
    steps = [
        f"Question: {num1} × 99",
        f"Step 1: Reduce the number by 1 -> {num1} - 1 = {left}",
        f"Step 2: Calculate complement from 100 -> 100 - {num1} = {right}",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_15(num1, num2):
    ans = num1 * num2
    steps = [
        f"Question: {num1} × {num2}",
        f"Step 1: Product = {ans}",
        "Step 2: Verify digit sum.",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_16(num1, num2):
    b = num1 + num2
    c = num1 * num2
    ans = f"x² + {b}x + {c}"
    steps = [
        f"Question: (x + {num1})(x + {num2})",
        f"Step 1: Sum of constants -> {num1} + {num2} = {b}",
        f"Step 2: Product of constants -> {num1} × {num2} = {c}",
        f"Correct Answer = {ans}"
    ]
    return {"success": True, "result": ans, "steps": steps}

def solve_sutra(sutra_id, num1, num2=0):
    solvers = {
        1: solve_sutra_1, 2: solve_sutra_2, 3: solve_sutra_3, 4: solve_sutra_4,
        5: solve_sutra_5, 6: solve_sutra_6, 7: solve_sutra_7, 8: solve_sutra_8,
        9: solve_sutra_9, 10: solve_sutra_10, 11: solve_sutra_11, 12: solve_sutra_12,
        13: solve_sutra_13, 14: solve_sutra_14, 15: solve_sutra_15, 16: solve_sutra_16
    }
    solver = solvers.get(sutra_id)
    return solver(num1, num2) if solver else {"success": False, "message": "Solver not found."}


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute(
            "SELECT id FROM students WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()

            flash("Email already exists.")
            return redirect(url_for("register"))

        # Insert new user
        cursor.execute(
            """
            INSERT INTO students (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (name, email, password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Registration Successful. Please login.")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password, profile_pic
            FROM students
            WHERE email = %s AND password = %s
            """,
            (email, password)
        )

        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if student:

            session.clear()

            # Store logged-in user's database ID
            session["student_id"] = student["id"]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, email, profile_pic FROM students WHERE id = %s",
        (student_id,)
    )
    student = cursor.fetchone()
    cursor.close()
    conn.close()

    if not student:
        session.clear()
        return redirect(url_for("login"))

    response = make_response(render_template("dashboard.html", student=student))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@app.route("/profile")
def profile():

    # User login nahi hai
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, profile_pic
            FROM students
            WHERE id = %s
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        # User database mein nahi mila
        if not student:
            session.clear()
            return redirect(url_for("login"))

        return render_template(
            "profile.html",
            student=student
        )

    except Exception as e:

        print("PROFILE ERROR:", e)

        return "Profile Error", 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/sutras")
def sutras_page():
    return render_template("sutras.html", sutras=sutras_list)

@app.route("/sutra/<int:id>", methods=["GET", "POST"])
def sutra_detail(id):
    sutra = next((s for s in sutras_list if s["id"] == id), None)
    if sutra is None:
        return "Sutra Not Found", 404

    previous_sutra = id - 1 if id > 1 else None
    next_sutra = id + 1 if id < 16 else None
    result, steps, success, message, hint = None, [], False, None, None

    if request.method == "POST":
        num1_text = request.form.get("num1", "").strip()
        num2_text = request.form.get("num2", "").strip()

        try:
            if not num1_text:
                raise ValueError
            num1 = int(num1_text)
            num2 = int(num2_text) if num2_text else 0
        except ValueError:
            success = False
            message = "❌ Please enter valid numbers."
            hint = "Only numeric values are allowed."
        else:
            solution = solve_sutra(id, num1, num2)
            success = solution.get("success", False)
            result = solution.get("result")
            steps = solution.get("steps", [])
            message = solution.get("message")
            hint = solution.get("hint")

    return render_template(
        "sutra_detail.html",
        sutra=sutra,
        result=result,
        steps=steps,
        success=success,
        message=message,
        hint=hint,
        previous_sutra=previous_sutra,
        next_sutra=next_sutra,
    )

# ============================================================
# PRACTICE MAIN PAGE (All 16 Sutras Selection Grid)
# ============================================================

@app.route("/practice")
def practice_main():
    return render_template("practice.html", all_sutras=sutras_list)

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get logged-in user's data
        cursor.execute(
            """
            SELECT id, name, email, profile_pic
            FROM students
            WHERE id = %s
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            session.clear()
            return redirect(url_for("login"))

        # Update profile
        if request.method == "POST":

            name = request.form.get("name", "").strip()

            if not name:
                flash("Please enter your name.")

                return render_template(
                    "edit_profile.html",
                    student=student
                )

            if len(name) < 2:
                flash("Name must contain at least 2 characters.")

                return render_template(
                    "edit_profile.html",
                    student=student
                )

            if len(name) > 50:
                flash("Name cannot be longer than 50 characters.")

                return render_template(
                    "edit_profile.html",
                    student=student
                )

            # By default keep the existing photo unless a new one is uploaded
            profile_pic_filename = student.get("profile_pic")

            print("DEBUG >>> request.files keys:", list(request.files.keys()))   # ADD THIS

            photo = request.files.get("photo")

            print("DEBUG >>> photo object:", photo)                              # ADD THIS
            if photo:
                print("DEBUG >>> photo.filename:", repr(photo.filename))         # ADD THIS

            if photo and photo.filename != "":

                if not allowed_file(photo.filename):
                    flash("Invalid image format. Use PNG, JPG, JPEG, GIF or WEBP.")
                    return render_template("edit_profile.html", student=student)

                filename = secure_filename(f"student_{student_id}_{photo.filename}")
                print("DEBUG >>> saving as:", filename)                          # ADD THIS

                save_path = os.path.join(UPLOAD_FOLDER, filename)
                print("DEBUG >>> save_path:", os.path.abspath(save_path))        # ADD THIS

                photo.save(save_path)

                print("DEBUG >>> file exists after save:", os.path.exists(save_path))  # ADD THIS

                profile_pic_filename = filename

            # Update MySQL
            cursor.execute(
                """
                UPDATE students
                SET name = %s, profile_pic = %s
                WHERE id = %s
                """,
                (name, profile_pic_filename, student_id)
            )

            conn.commit()

            flash("Profile updated successfully!")

            return redirect(url_for("profile"))

        # Open edit_profile.html
        return render_template(
            "edit_profile.html",
            student=student
        )

    except Exception as e:

        if conn:
            conn.rollback()

        print("EDIT PROFILE ERROR:", e)

        return "Edit Profile Error", 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ============================================================
# PRACTICE DETAILS PAGE (20 Questions Form - Photo Layout)
# ============================================================

@app.route("/practice/<int:id>", methods=["GET", "POST"])
def practice(id):
    sutra = next((s for s in sutras_list if s["id"] == id), None)
    if sutra is None:
        return "Sutra Not Found", 404

    questions = generate_20_questions(id)
    submitted_q = None

    if request.method == "POST":
        try:
            q_id = int(request.form.get("question_id", 0))
            num1 = int(request.form.get("num1", 0))
            num2 = int(request.form.get("num2", 0))
            user_ans = request.form.get("user_ans", "").strip()
        except ValueError:
            submitted_q = {
                "id": 0,
                "is_correct": False,
                "user_ans": "",
                "correct_ans": "",
                "steps": ["❌ Please enter valid numbers."],
            }
        else:
            solution = solve_sutra(id, num1, num2)
            correct_ans = solution.get("result", "")
            is_correct = str(user_ans).strip() == str(correct_ans).strip()

            submitted_q = {
                "id": q_id,
                "user_ans": user_ans,
                "correct_ans": correct_ans,
                "is_correct": is_correct,
                "steps": solution.get("steps", []),
                "message": solution.get("message"),
            }

    return render_template(
        "practice_details.html",
        sutra=sutra,
        all_sutras=sutras_list,
        questions=questions,
        submitted_q=submitted_q,
    )

@app.route("/ai-scan")
def ai_scan():
    return render_template("ai_scan.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/speed-test")
def speed_test():
    return render_template("speed_test.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )