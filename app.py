import os
import base64
import secrets
import random
import mysql.connector
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from flask_mail import Mail, Message

load_dotenv()

from datetime import datetime, timedelta


from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask import make_response
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

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

print("KEY LOADED:", os.environ.get("GEMINI_API_KEY"))
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.5-flash")

GOOGLE_CLIENT_ID = "976524200976-9rkjn3etb9qgnvpp5vsvfo5v2uclqadb.apps.googleusercontent.com"

# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
app.secret_key = "vedic-maths-secret-key-2026"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)


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
        "name": "Sopantyadvaya-"
        "mantyam",
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
    if num1 % 10 != 5:
        return {
            "success": False,
            "error": "Ekadhikena Purvena Formula Only assign to the last digit 5 numbers (e.g., 15, 25, 35)!"
        }
    
    n = num1 // 10 
    next_num = n + 1
    left = n * next_num
    answer = (left * 100) + 25 
    
    steps = [
        "Step 1: The last digit is 5, so the end of the answer will be 25.",
        f"Step 2: Multiply the remaining part ({n}) by its next consecutive integer ({next_num}) -> {n} × {next_num} = {left}",
        f"Step 3: Combine both parts together -> {left}25",
        f"Correct Answer = {answer}"
    ]
    
    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_2(num1, num2):
    base = 100
    dev1 = num1 - base
    dev2 = num2 - base
    
    cross_op = num1 + dev2 
    
    prod = dev1 * dev2
    
    answer = num1 * num2
    
    sign1 = "+" if dev1 > 0 else "-"
    sign2 = "+" if dev2 > 0 else "-"

    steps = [
        f"Step 1: Calculate deviation from base {base}: {num1} is ({sign1}{abs(dev1)}) and {num2} is ({sign2}{abs(dev2)}).",
        f"Step 2: Perform cross operation (Number 1 + Deviation 2) -> {num1} + ({sign2}{abs(dev2)}) = {cross_op}.",
        f"Step 3: Multiply the deviations -> {abs(dev1)} × {abs(dev2)} = {prod:02d} (padded to 2 digits for base 100).",
        f"Step 4: Combine the left and right parts -> {cross_op}{prod:02d}",
        f"Final Answer = {answer}"
    ]
    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_3(num1, num2):
    if not (10 <= num1 <= 99 and 10 <= num2 <= 99):
        return {
            "success": True, 
            "result": str(num1 * num2), 
            "steps": [f"Direct Multiplication: {num1} × {num2} = {num1 * num2}"]
        }

    a, b = num1 // 10, num1 % 10
    c, d = num2 // 10, num2 % 10

    step1_prod = b * d
    unit_digit = step1_prod % 10
    carry1 = step1_prod // 10

    cross_sum = (a * d) + (b * c)
    step2_total = cross_sum + carry1
    tens_digit = step2_total % 10
    carry2 = step2_total // 10

    step3_prod = a * c
    hundreds_part = step3_prod + carry2

    answer = num1 * num2

    steps = [
        f"Step 1 (Right Vertical): {b} × {d} = {step1_prod} → Keep {unit_digit}, Carry = {carry1}",
        f"Step 2 (Crosswise): ({a} × {d}) + ({b} × {c}) = {cross_sum}. Add carry: {cross_sum} + {carry1} = {step2_total} → Keep {tens_digit}, Carry = {carry2}",
        f"Step 3 (Left Vertical): ({a} × {c}) = {step3_prod}. Add carry: {step3_prod} + {carry2} = {hundreds_part}",
        f"Step 4 (Combine): [{hundreds_part}][{tens_digit}][{unit_digit}]",
        f"Final Answer = {answer}"
    ]

    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_4(num1, num2):
    # Condition Check: Prevent division by zero
    if num2 == 0:
        return {"success": False, "message": "Division by zero is not allowed."}

    q, r = divmod(num1, num2)

    # Determine nearest base (10, 100, etc.) for the divisor
    if num2 < 10:
        base = 10
    else:
        base = 10 ** (len(str(num2)) - 1)

    deviation = num2 - base
    transposed_dev = -deviation

    result_str = f"Quotient = {q}, Remainder = {r}" if r != 0 else str(q)

    steps = [
        f"Question: {num1} ÷ {num2}",
        f"Step 1 (Find Base & Deviation): Divisor = {num2}, Base = {base} → Deviation = {deviation:+d}",
        f"Step 2 (Transpose): Reverse the sign of the deviation → Transposed multiplier = {transposed_dev:+d}",
        f"Step 3 (Apply Multiplier): Multiply digits by {transposed_dev:+d} across columns to separate quotient from remainder.",
        f"Step 4 (Calculate): Quotient = {q}" + (f", Remainder = {r}" if r else " (Exact Division)"),
        f"Final Answer = {result_str}"
    ]

    return {"success": True, "result": result_str, "steps": steps}

def solve_sutra_5(num1, num2):
    # Solves linear equations of the form: x + num2 = num1
    # Condition: Applicable for linear algebraic equations where terms balance to zero
    
    ans = num1 - num2
    
    steps = [
        f"Equation: x + {num2} = {num1}",
        f"Step 1 (Apply Sutra): Express as sum equated to zero -> x + ({num2} - {num1}) = 0",
        f"Step 2 (Simplify Constant): x + ({num2 - num1}) = 0",
        f"Step 3 (Solve for x): Transpose constant term -> x = {ans}",
        f"Final Answer = x = {ans}"
    ]
    
    return {
        "success": True, 
        "result": f"x = {ans}", 
        "steps": steps
    }

def solve_sutra_6(num1, num2):
    # Determine working base (WB) and ratio multiplier (k) relative to primary base (100)
    # Defaulting to Working Base 50 (WB = 100 / 2 => k = 0.5)
    primary_base = 100
    working_base = 50
    k = working_base / primary_base  # Ratio factor = 0.5

    # Calculate deviations from the working base
    dev1 = num1 - working_base
    dev2 = num2 - working_base

    # Step-by-step components
    cross_sum = num1 + dev2
    adjusted_left = cross_sum * k  # Scale by ratio factor k
    right_prod = dev1 * dev2

    answer = num1 * num2

    sign1 = "+" if dev1 >= 0 else "-"
    sign2 = "+" if dev2 >= 0 else "-"

    steps = [
        f"Question: {num1} × {num2}",
        f"Step 1 (Select Working Base): Take Working Base = {working_base} (Primary Base {primary_base} × {k}).",
        f"Step 2 (Find Deviations): {num1} is ({sign1}{abs(dev1)}) and {num2} is ({sign2}{abs(dev2)}) from {working_base}.",
        f"Step 3 (Cross Operation): {num1} + ({dev2:+d}) = {cross_sum}.",
        f"Step 4 (Proportional Adjustment): Multiply cross sum by factor {k} → {cross_sum} × {k} = {adjusted_left:g}.",
        f"Step 5 (Multiply Deviations): ({dev1:+d}) × ({dev2:+d}) = {right_prod:02d}.",
        f"Step 6 (Combine): Combine adjusted left part with right product → {adjusted_left:g} | {right_prod:02d}.",
        f"Final Answer = {answer}"
    ]

    return {"success": True, "result": str(answer), "steps": steps}

def solve_sutra_7(num1, num2):
    # Condition: Treats num1 as (x + y) and num2 as (x - y)
    # Solves for x and y using simultaneous addition and subtraction
    
    sum_val = num1
    diff_val = num2

    x = (sum_val + diff_val) / 2
    y = (sum_val - diff_val) / 2

    # Format output integers if whole numbers
    x_str = int(x) if x.is_integer() else x
    y_str = int(y) if y.is_integer() else y

    steps = [
        f"Given: Sum (x + y) = {sum_val}, Difference (x - y) = {diff_val}",
        f"Step 1 (Sankalana - Addition): Add both equations -> (x + y) + (x - y) = {sum_val} + {diff_val} => 2x = {sum_val + diff_val}",
        f"Step 2 (Find x): x = {sum_val + diff_val} ÷ 2 = {x_str}",
        f"Step 3 (Vyavakalana - Subtraction): Subtract both equations -> (x + y) - (x - y) = {sum_val} - {diff_val} => 2y = {sum_val - diff_val}",
        f"Step 4 (Find y): y = {sum_val - diff_val} ÷ 2 = {y_str}",
        f"Final Answer = x = {x_str}, y = {y_str}"
    ]

    return {
        "success": True, 
        "result": f"x = {x_str}, y = {y_str}", 
        "steps": steps
    }

def solve_sutra_8(num1, num2):
    # Condition: Best used when one number is close to a multiple of 10 (ends in 7, 8, 9)
    ans = num1 + num2

    # Find remainder modulo 10 to check proximity to next multiple of 10
    rem1 = num1 % 10
    rem2 = num2 % 10

    # Pick the number closer to completing a ten (higher remainder)
    if (10 - rem1) <= (10 - rem2) and rem1 != 0:
        target, helper = num1, num2
    else:
        target, helper = num2, num1

    deficiency = (10 - (target % 10)) % 10

    if deficiency == 0:
        # Fallback if both numbers already end in 0
        steps = [
            f"Question: {num1} + {num2}",
            f"Step 1: Numbers are already multiples of 10.",
            f"Step 2: Add directly -> {num1} + {num2} = {ans}",
            f"Final Answer = {ans}"
        ]
    else:
        completed_target = target + deficiency
        remaining_helper = helper - deficiency

        steps = [
            f"Question: {num1} + {num2}",
            f"Step 1 (Identify Base Completion): {target} needs {deficiency} to complete to {completed_target}.",
            f"Step 2 (Borrow Deficit): Borrow {deficiency} from {helper} → ({helper} - {deficiency}) = {remaining_helper}.",
            f"Step 3 (Add Completed Base): Combine completed base with remainder → {completed_target} + {remaining_helper} = {ans}",
            f"Final Answer = {ans}"
        ]

    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_9(num1, num2):
    # Condition: Evaluates absolute variance/difference between two numbers
    diff = num1 - num2
    ans = abs(diff)

    steps = [
        f"Question: Find difference between {num1} and {num2} -> |{num1} - {num2}|",
        f"Step 1 (Sequential Difference): Calculate raw change -> {num1} - {num2} = {diff}",
        f"Step 2 (Apply Chalana Kalanabhyam): Evaluate absolute magnitude -> |{diff}| = {ans}",
        f"Final Answer = {ans}"
    ]

    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_10(num1, num2=0):
    # Condition: Best used for squaring numbers close to a base (10, 100, 1000)
    
    # Dynamically determine the base
    num_str = str(abs(num1))
    digits = len(num_str)
    base = 10 ** digits if num1 > (10 ** digits) / 2 else 10 ** (digits - 1)
    if base < 10:
        base = 10

    base_zeros = len(str(base)) - 1
    dev = num1 - base  # Deviation: Negative for deficiency, positive for surplus

    left_part = num1 + dev
    right_part = dev ** 2
    ans = num1 * num1

    # Format the right part to match the number of zeros in the base
    right_str = f"{right_part:0{base_zeros}d}"

    sign_str = "deficiency" if dev < 0 else "surplus"

    steps = [
        f"Question: {num1}²",
        f"Step 1 (Find Base & Deviation): Base = {base}, Deviation ({sign_str}) = {dev:+d}",
        f"Step 2 (Left Part): Add deviation to the number -> {num1} + ({dev:+d}) = {left_part}",
        f"Step 3 (Right Part): Square the deviation -> ({dev:+d})² = {right_str}",
        f"Step 4 (Combine): Join left and right parts -> {left_part}{right_str}",
        f"Final Answer = {ans}"
    ]

    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_11(num1, num2):
    # Condition: Best applied by splitting one factor into place-value parts (tens + units)
    ans = num1 * num2

    # Split num2 into tens and units parts
    tens_part = (num2 // 10) * 10
    units_part = num2 % 10

    if tens_part == 0 or units_part == 0:
        # Fallback if num2 is a single digit or pure multiple of 10
        steps = [
            f"Question: {num1} × {num2}",
            f"Step 1: Direct multiplication -> {num1} × {num2} = {ans}",
            f"Final Answer = {ans}"
        ]
    else:
        prod1 = num1 * tens_part
        prod2 = num1 * units_part

        steps = [
            f"Question: {num1} × {num2}",
            f"Step 1 (Vyasti - Split into Parts): Split {num2} into ({tens_part} + {units_part})",
            f"Step 2 (Partial Product 1): {num1} × {tens_part} = {prod1}",
            f"Step 3 (Partial Product 2): {num1} × {units_part} = {prod2}",
            f"Step 4 (Samashti - Combine Whole): Add partial products -> {prod1} + {prod2} = {ans}",
            f"Final Answer = {ans}"
        ]

    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_12(num1, num2):
    # Condition: Prevent division by zero
    if num2 == 0:
        return {"success": False, "message": "Division by zero is not allowed."}

    q = num1 // num2  # Integer Quotient
    prod = q * num2   # Product of Quotient and Divisor
    r = num1 - prod   # Remainder calculation

    steps = [
        f"Question: Find Remainder of {num1} ÷ {num2}",
        f"Step 1 (Find Quotient): {num1} ÷ {num2} gives Quotient (Q) = {q}",
        f"Step 2 (Multiply Quotient by Divisor): {q} × {num2} = {prod}",
        f"Step 3 (Calculate Remainder): Dividend - (Quotient × Divisor) -> {num1} - {prod} = {r}",
        f"Final Answer = Remainder {r}"
    ]

    return {"success": True, "result": f"R = {r}", "steps": steps}

def solve_sutra_13(num1, num2):
    # Condition: Evaluates expressions combining ultimate term (num1) and twice penultimate term (num2) -> num1 + 2(num2)
    
    double_penultimate = 2 * num2
    ans = num1 + double_penultimate

    steps = [
        f"Question: {num1} + 2({num2})",
        f"Step 1 (Twice Penultimate): Double the second term -> 2 × {num2} = {double_penultimate}",
        f"Step 2 (Add Ultimate): Add ultimate term to doubled value -> {num1} + {double_penultimate} = {ans}",
        f"Final Answer = {ans}"
    ]

    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_14(num1, num2=99):
    # Condition: Check if multiplier (num2) consists entirely of 9s
    multiplier_str = str(num2)
    if not set(multiplier_str).issubset({'9'}):
        # Fallback if num2 is not made of 9s
        ans = num1 * num2
        return {
            "success": True, 
            "result": str(ans), 
            "steps": [f"Direct Multiplication: {num1} × {num2} = {ans}"]
        }

    left = num1 - 1
    right = num2 - left
    ans = num1 * num2

    # Format right part with leading zero padding matching the digit count of the 9s
    num_nines = len(multiplier_str)
    right_str = f"{right:0{num_nines}d}"

    steps = [
        f"Question: {num1} × {num2}",
        f"Step 1 (Ekanyunena - One Less): Reduce {num1} by 1 -> {num1} - 1 = {left}",
        f"Step 2 (Complement): Subtract left part from multiplier -> {num2} - {left} = {right_str}",
        f"Step 3 (Combine): Join left and right parts -> {left}{right_str}",
        f"Final Answer = {ans}"
    ]

    return {"success": True, "result": str(ans), "steps": steps}

def digital_root(n):
    """Helper function to calculate single-digit sum (digital root)."""
    n = abs(n)
    while n >= 10:
        n = sum(int(digit) for digit in str(n))
    return n

def solve_sutra_15(num1, num2):
    # Condition: Verifies multiplication correctness via digital roots (Digit Sums)
    ans = num1 * num2

    sd1 = digital_root(num1)
    sd2 = digital_root(num2)
    sd_prod_inputs = digital_root(sd1 * sd2)
    sd_actual_ans = digital_root(ans)

    is_verified = (sd_prod_inputs == sd_actual_ans)

    steps = [
        f"Question: Multiply {num1} × {num2}",
        f"Step 1 (Calculate Product): {num1} × {num2} = {ans}",
        f"Step 2 (Digit Sum of Factors): SD({num1}) = {sd1}, SD({num2}) = {sd2}",
        f"Step 3 (Product of Digit Sums): {sd1} × {sd2} = {sd1 * sd2} → Digital Root = {sd_prod_inputs}",
        f"Step 4 (Digit Sum of Final Product): SD({ans}) = {sd_actual_ans}",
        f"Step 5 (Verification Check): {sd_prod_inputs} == {sd_actual_ans} → {'Verified Correct' if is_verified else 'Mismatch Found'}",
        f"Final Answer = {ans}"
    ]

    return {"success": True, "result": str(ans), "steps": steps}

def solve_sutra_16(num1, num2):
    # Condition: Expands binomials (x + num1)(x + num2) -> x² + bx + c
    
    b = num1 + num2
    c = num1 * num2

    # Format middle term (+ bx or - bx)
    if b > 0:
        b_str = f" + {b}x"
    elif b < 0:
        b_str = f" - {abs(b)}x"
    else:
        b_str = ""

    # Format constant term (+ c or - c)
    if c > 0:
        c_str = f" + {c}"
    elif c < 0:
        c_str = f" - {abs(c)}"
    else:
        c_str = ""

    ans = f"x²{b_str}{c_str}"

    sign1 = f"+ {num1}" if num1 >= 0 else f"- {abs(num1)}"
    sign2 = f"+ {num2}" if num2 >= 0 else f"- {abs(num2)}"

    steps = [
        f"Question: Expand (x {sign1})(x {sign2})",
        f"Step 1 (Sum of Constants for 'x' term): {num1} + ({num2}) = {b}",
        f"Step 2 (Product of Constants): {num1} × ({num2}) = {c}",
        f"Step 3 (Combine into Quadratic Form): x² + ({b})x + ({c})",
        f"Final Answer = {ans}"
    ]

    return {"success": True, "result": ans, "steps": steps}


def solve_sutra(sutra_id, num1, num2=0):
    solvers = {
        1: solve_sutra_1, 2: solve_sutra_2, 3: solve_sutra_3, 4: solve_sutra_4,
        5: solve_sutra_5, 6: solve_sutra_6, 7: solve_sutra_7, 8: solve_sutra_8,
        9: solve_sutra_9, 10: solve_sutra_10, 11: solve_sutra_11, 12: solve_sutra_12,
        13: solve_sutra_13, 14: solve_sutra_14, 15: solve_sutra_15, 16: solve_sutra_16
    }
    # Integer conversion safeguard
    try:
        sutra_id = int(sutra_id)
    except (ValueError, TypeError):
        return {"success": False, "message": "Invalid Sutra ID."}

    solver = solvers.get(sutra_id)
    return solver(num1, num2) if solver else {"success": False, "message": "Solver not found."}


def update_streak(cursor, student_id):
    cursor.execute(
        "SELECT last_active_date, current_streak FROM students WHERE id = %s",
        (student_id,)
    )
    row = cursor.fetchone()

    if not row:
        return

    today = date.today()
    last_active = row.get("last_active_date") if isinstance(row, dict) else row[0]
    current_streak = (row.get("current_streak") if isinstance(row, dict) else row[1]) or 0

    # Ensure last_active is a date object if DB returns string
    if isinstance(last_active, str):
        try:
            last_active = date.fromisoformat(last_active)
        except ValueError:
            last_active = None

    if last_active == today:
        return

    if last_active == today - timedelta(days=1):
        new_streak = current_streak + 1
    else:
        new_streak = 1

    cursor.execute(
        "UPDATE students SET last_active_date = %s, current_streak = %s WHERE id = %s",
        (today, new_streak, student_id)
    )


def get_practice_stats(cursor, student_id):
    cursor.execute("""
        SELECT sutra_id, COUNT(*) AS attempted, COALESCE(SUM(is_correct), 0) AS correct
        FROM practice_answers
        WHERE student_id = %s
        GROUP BY sutra_id
    """, (student_id,))

    rows = cursor.fetchall() or []

    total_attempts = 0
    total_correct = 0
    sutras_mastered = 0

    for r in rows:
        attempted = r["attempted"] if isinstance(r, dict) else r[1]
        correct = (r["correct"] if isinstance(r, dict) else r[2]) or 0

        total_attempts += attempted
        total_correct += int(correct)

        if attempted >= MIN_ATTEMPTS_FOR_MASTERY and (correct / attempted) >= MASTERY_THRESHOLD:
            sutras_mastered += 1

    return {
        "total_attempts": total_attempts,
        "correct_attempts": total_correct,
        "sutras_attempted": len(rows),
        "sutras_mastered": sutras_mastered,
    }

# ============================================================
# ROUTES
# ============================================================

QUIZ_TOTAL_QUESTIONS = 55
TOTAL_SUTRAS = 16

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

@app.route("/google_login", methods=["POST"])
def google_login():
    data = request.get_json(silent=True) or {}
    token = data.get("credential")

    if not token:
        return jsonify({"success": False, "message": "No credential provided."}), 400

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

        if not idinfo.get("email_verified"):
            return jsonify({"success": False, "message": "Email not verified by Google."}), 400

        email = idinfo["email"]
        name = idinfo.get("name", "")
        photo = idinfo.get("picture", "")

    except ValueError:
        return jsonify({"success": False, "message": "Invalid Google token."}), 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM students WHERE email = %s", (email,))
        student = cursor.fetchone()

        if student:
            student_id = student["id"]
        else:
            cursor.execute(
                "INSERT INTO students (name, email, password, profile_pic) VALUES (%s, %s, %s, %s)",
                (name, email, "", photo)
            )
            conn.commit()
            student_id = cursor.lastrowid

        session.clear()
        session["student_id"] = student_id

        return jsonify({"success": True, "redirect": url_for("dashboard")})

    except Exception as e:
        if conn:
            conn.rollback()
        print("GOOGLE LOGIN ERROR:", e)
        return jsonify({"success": False, "message": "Server error, try again."}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM students WHERE email = %s", (email,))
        student = cursor.fetchone()

        if student:
            # Token generate karo
            token = secrets.token_urlsafe(32)
            expiry = datetime.utcnow() + timedelta(hours=1)

            # DB me save karo
            cursor.execute("""
                UPDATE students 
                SET reset_token = %s, reset_token_expiry = %s 
                WHERE email = %s
            """, (token, expiry, email))
            conn.commit()

            # Reset link email karo
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message(
                subject="VedicMath - Password Reset",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[email]
            )
            msg.body = f"Password reset link (valid 1 hour):\n\n{reset_link}"
            mail.send(msg)

        cursor.close()
        conn.close()

        # Email exist kare ya na kare — same message dikho (security)
        flash("If this email exists, a reset link has been sent.")
        return redirect(url_for('forgot_password'))

    return render_template("forgot_password.html")

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id FROM students 
        WHERE reset_token = %s AND reset_token_expiry > %s
    """, (token, datetime.utcnow()))
    student = cursor.fetchone()

    if not student:
        cursor.close()
        conn.close()
        flash("Reset link is invalid or expired.")
        return redirect(url_for('login'))

    if request.method == "POST":
        new_password = request.form.get("password", "").strip()

        if len(new_password) < 6:
            flash("Password must be at least 6 characters.")
            return render_template("reset_password.html", token=token)

        cursor.execute("""
            UPDATE students 
            SET password = %s, reset_token = NULL, reset_token_expiry = NULL 
            WHERE id = %s
        """, (new_password, student["id"]))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Password updated! Please login.")
        return redirect(url_for('login'))

    cursor.close()
    conn.close()
    return render_template("reset_password.html", token=token)

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
 
    if not student:
        cursor.close()
        conn.close()
        session.clear()
        return redirect(url_for("login"))
 
    practice_stats = get_practice_stats(cursor, student_id)
 
    total_attempts = practice_stats["total_attempts"]
    correct_attempts = practice_stats["correct_attempts"]
    accuracy = round((correct_attempts / total_attempts) * 100, 1) if total_attempts > 0 else 0
    sutras_mastered = practice_stats["sutras_mastered"]
 
    stats = {
        "total_attempts": total_attempts,
        "correct_attempts": correct_attempts,
        "accuracy": accuracy,
        "sutras_mastered": sutras_mastered,
    }
 
    cursor.close()
    conn.close()
 
    return render_template("dashboard.html", student=student, stats=stats)

@app.route("/profile")
def profile():
 
    if "student_id" not in session:
        return redirect(url_for("login"))
 
    student_id = session["student_id"]
 
    conn = None
    cursor = None
 
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        cursor.execute("""
            SELECT id, name, email, profile_pic, current_streak
            FROM students
            WHERE id = %s
        """, (student_id,))
 
        student = cursor.fetchone()
 
        if not student:
            session.clear()
            return redirect(url_for("login"))
 
        # ---- QUIZ stats (student_answers) ----
        cursor.execute("""
            SELECT COUNT(*) AS attempted, COALESCE(SUM(is_correct), 0) AS correct
            FROM student_answers
            WHERE student_id = %s
        """, (student_id,))
        quiz_stats = cursor.fetchone()
 
        # ---- PRACTICE stats (practice_answers) ----
        practice_stats = get_practice_stats(cursor, student_id)
 
        # ---- COMBINE both ----
        total_attempted = (quiz_stats["attempted"] or 0) + practice_stats["total_attempts"]
        total_correct = (quiz_stats["correct"] or 0) + practice_stats["correct_attempts"]
 
        accuracy = round((total_correct / total_attempted) * 100, 1) if total_attempted > 0 else 0
 
        sutras_mastered = practice_stats["sutras_mastered"]
        overall_progress = round((sutras_mastered / TOTAL_SUTRAS) * 100, 1) if TOTAL_SUTRAS else 0
 
        stats = {
            "problems_solved": total_attempted,
            "accuracy": accuracy,
            "sutras_mastered": sutras_mastered,
            "overall_progress": overall_progress,
            "day_streak": student["current_streak"] or 0
        }
 
        return render_template("profile.html", student=student, stats=stats)
 
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
 
            if "student_id" in session:
                conn = None
                cursor = None
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor(dictionary=True)
 
                    cursor.execute(
                        """
                        INSERT INTO practice_answers
                            (student_id, sutra_id, question_id, user_answer, correct_answer, is_correct)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            session["student_id"],
                            id,
                            q_id,
                            user_ans,
                            correct_ans,
                            1 if is_correct else 0,
                        )
                    )
 
                    # ---- NAYI LINE: streak update ----
                    update_streak(cursor, session["student_id"])
 
                    conn.commit()
                except Exception as e:
                    if conn:
                        conn.rollback()
                    print("PRACTICE SAVE ERROR:", e)
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
 
    return render_template(
        "practice_details.html",
        sutra=sutra,
        all_sutras=sutras_list,
        questions=questions,
        submitted_q=submitted_q,
    )

@app.route("/ai-scan", methods=["GET", "POST"])
def ai_scan():
    result = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        image_file = request.files.get("image")
        camera_data = request.form.get("camera_image")

        pil_image = None

        if image_file and image_file.filename != "":
            pil_image = Image.open(image_file.stream)

        elif camera_data:
            # camera_data format: "data:image/png;base64,xxxxx"
            header, encoded = camera_data.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            pil_image = Image.open(BytesIO(image_bytes))

        system_instruction = (
            "You are a Vedic Mathematics tutor. Solve the given maths problem in a simple, clean format.\n\n"
            "Rules:\n"
            "- NO markdown, NO LaTeX, NO symbols like ** or $$ or ```\n"
            "- Write in plain simple English\n"
            "- Use this exact format:\n\n"
            "Let's solve [problem] with a detailed explanation.\n"
            "Step 1: [step title]\n"
            "[explanation]\n"
            "Step 2: [step title]\n"
            "[explanation]\n"
            "... and so on\n\n"
            "Final Answer\n"
            "[problem] = [answer]\n\n"
            "Quick Vedic Math Trick\n"
            "[one short alternative trick if applicable]\n\n"
            "Answer = [answer]\n\n"
            "Keep it short, clear and beginner-friendly. No long paragraphs."
        )

        content_parts = [system_instruction]
        if prompt:
            content_parts.append(prompt)
        if pil_image:
            content_parts.append(pil_image)

        if len(content_parts) == 1:  # sirf system instruction hai, kuch input nahi
            result = "Please enter a question or upload an image."
        else:
            try:
                response = model.generate_content(content_parts)
                result = response.text
            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("ai_scan.html", result=result)

@app.route("/quiz")
def quiz():
    student_id = session.get("student_id")
    if not student_id:
        return redirect(url_for("login"))

    quiz_id = 1
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT total_questions, attempted_questions, correct_answers,
                   wrong_answers, progress_percentage, current_question, status
            FROM quiz_attempts
            WHERE student_id = %s AND quiz_id = %s
        """, (student_id, quiz_id))

        attempt = cursor.fetchone()

        if not attempt:
            cursor.execute("""
                INSERT INTO quiz_attempts
                    (student_id, quiz_id, current_question, total_questions, status, started_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (student_id, quiz_id, 1, QUIZ_TOTAL_QUESTIONS, "in_progress"))

            conn.commit()

            attempt = {
                "total_questions": QUIZ_TOTAL_QUESTIONS,
                "attempted_questions": 0,
                "correct_answers": 0,
                "wrong_answers": 0,
                "progress_percentage": 0,
                "current_question": 1,
                "status": "in_progress"
            }

        return render_template("quiz.html", attempt=attempt)

    except Exception as e:
        if conn:
            conn.rollback()
        print("QUIZ ERROR:", e)
        return "Quiz Error", 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    student_id = session.get("student_id")
    if not student_id:
        return jsonify({"error": "unauthorized"}), 401
 
    data = request.get_json(silent=True) or {}
    quiz_id = data.get("quiz_id", 1)
    question_index = data.get("question_index")
    selected_option = data.get("selected_option")
    is_correct = 1 if data.get("is_correct") else 0
 
    if question_index is None or selected_option is None:
        return jsonify({"error": "missing fields"}), 400
 
    conn = None
    cursor = None
 
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        cursor.execute("""
            SELECT id FROM student_answers
            WHERE student_id = %s AND quiz_id = %s AND question_index = %s
        """, (student_id, quiz_id, question_index))
        existing = cursor.fetchone()
 
        if existing:
            cursor.execute("""
                UPDATE student_answers
                SET selected_option = %s, is_correct = %s, answered_at = NOW()
                WHERE id = %s
            """, (selected_option, is_correct, existing["id"]))
        else:
            cursor.execute("""
                INSERT INTO student_answers
                    (student_id, quiz_id, question_index, selected_option, is_correct)
                VALUES (%s, %s, %s, %s, %s)
            """, (student_id, quiz_id, question_index, selected_option, is_correct))
 
        # ---- NAYI LINE: streak update ----
        update_streak(cursor, student_id)
 
        conn.commit()
 
        cursor.execute("""
            SELECT COUNT(*) AS attempted, COALESCE(SUM(is_correct), 0) AS correct
            FROM student_answers
            WHERE student_id = %s AND quiz_id = %s
        """, (student_id, quiz_id))
        agg = cursor.fetchone()
 
        attempted = agg["attempted"] or 0
        correct = agg["correct"] or 0
        wrong = attempted - correct
 
        cursor.execute("""
            SELECT total_questions FROM quiz_attempts
            WHERE student_id = %s AND quiz_id = %s
        """, (student_id, quiz_id))
        row = cursor.fetchone()
        total_questions = row["total_questions"] if row else QUIZ_TOTAL_QUESTIONS
 
        progress = round((attempted / total_questions) * 100, 1) if total_questions else 0
        status = "completed" if attempted >= total_questions else "in_progress"
 
        cursor.execute("""
            UPDATE quiz_attempts
            SET attempted_questions = %s,
                correct_answers = %s,
                wrong_answers = %s,
                progress_percentage = %s,
                current_question = %s,
                status = %s
            WHERE student_id = %s AND quiz_id = %s
        """, (attempted, correct, wrong, progress, question_index + 1,
              status, student_id, quiz_id))
 
        conn.commit()
 
        return jsonify({
            "success": True,
            "attempted": attempted,
            "correct": correct,
            "wrong": wrong,
            "progress": progress
        })
 
    except Exception as e:
        if conn:
            conn.rollback()
        print("SUBMIT ANSWER ERROR:", e)
        return jsonify({"error": str(e)}), 500
 
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/speed-test")
def speed_test():
    return render_template("speed_test.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/leaderboard")
def leaderboard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                s.id, 
                s.name, 
                s.profile_pic,
                s.current_streak,
                COALESCE(qa.correct, 0) + COALESCE(pa.correct, 0) AS total_correct,
                COALESCE(qa.attempted, 0) + COALESCE(pa.attempted, 0) AS total_attempted
            FROM students s
            LEFT JOIN (
                SELECT student_id, COUNT(*) AS attempted, SUM(is_correct) AS correct
                FROM student_answers
                GROUP BY student_id
            ) qa ON qa.student_id = s.id
            LEFT JOIN (
                SELECT student_id, COUNT(*) AS attempted, SUM(is_correct) AS correct
                FROM practice_answers
                GROUP BY student_id
            ) pa ON pa.student_id = s.id
            HAVING total_attempted > 0
            ORDER BY total_correct DESC, total_attempted ASC
            LIMIT 50
        """)

        rows = cursor.fetchall()

        leaderboard_data = []
        for idx, row in enumerate(rows, start=1):
            accuracy = round((row["total_correct"] / row["total_attempted"]) * 100, 1) if row["total_attempted"] else 0
            leaderboard_data.append({
                "rank": idx,
                "id": row["id"],
                "name": row["name"],
                "profile_pic": row["profile_pic"],
                "total_correct": row["total_correct"],
                "total_attempted": row["total_attempted"],
                "accuracy": accuracy,
                "streak": row["current_streak"] or 0,
            })

        current_student_id = session["student_id"]
        my_rank = next((e for e in leaderboard_data if e["id"] == current_student_id), None)

        return render_template(
            "leaderboard.html",
            leaderboard=leaderboard_data,
            my_rank=my_rank
        )

    except Exception as e:
        print("LEADERBOARD ERROR:", e)
        return "Leaderboard Error", 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


from datetime import date

@app.route("/formulas")
def vedic_formulas():
    return render_template("formulas.html", sutras=sutras_list)

@app.route("/challenge", methods=["GET", "POST"])
def daily_challenge():
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]
    today = date.today()

    # Aajcha sutra decide karnyasathi date-based rotation (16 sutras madhun)
    day_number = today.toordinal()
    sutra_id = (day_number % 16) + 1
    sutra = next((s for s in sutras_list if s["id"] == sutra_id), None)

    conn = None
    cursor = None
    result = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Aaj already solve kela ka check kar
        cursor.execute("""
            SELECT * FROM daily_challenges
            WHERE student_id = %s AND challenge_date = %s
        """, (student_id, today))
        existing = cursor.fetchone()

        if existing:
            return render_template(
                "daily_challenge.html",
                sutra=sutra,
                already_done=True,
                attempt=existing
            )

        # Student-specific random question (student_id + date seed)
        seed_value = student_id * 1000 + day_number
        random.seed(seed_value)
        questions = generate_20_questions(sutra_id)
        random.seed()  # reset global seed
        question = random.choice(questions)

        if request.method == "POST":
            user_ans = request.form.get("user_ans", "").strip()
            solution = solve_sutra(sutra_id, question["num1"], question["num2"])
            correct_ans = solution.get("result", "")
            is_correct = str(user_ans).strip() == str(correct_ans).strip()
            points = 10 if is_correct else 2  # try karnyasathi bhi thode points

            cursor.execute("""
                INSERT INTO daily_challenges
                    (student_id, challenge_date, sutra_id, question_text, user_answer, correct_answer, is_correct, points_earned)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (student_id, today, sutra_id, question["q_text"], user_ans, correct_ans, 1 if is_correct else 0, points))

            cursor.execute("""
                UPDATE students SET total_points = total_points + %s WHERE id = %s
            """, (points, student_id))

            conn.commit()

            result = {
                "is_correct": is_correct,
                "correct_ans": correct_ans,
                "points": points,
                "steps": solution.get("steps", [])
            }

            return render_template(
                "daily_challenge.html",
                sutra=sutra,
                already_done=True,
                attempt={
                    "user_answer": user_ans,
                    "correct_answer": correct_ans,
                    "is_correct": is_correct,
                    "points_earned": points
                },
                result=result
            )

        return render_template(
            "daily_challenge.html",
            sutra=sutra,
            question=question,
            already_done=False
        )

    except Exception as e:
        if conn:
            conn.rollback()
        print("DAILY CHALLENGE ERROR:", e)
        return "Daily Challenge Error", 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/certificates")
def certificates():
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name FROM students WHERE id = %s
        """, (student_id,))
        student = cursor.fetchone()

        if not student:
            session.clear()
            return redirect(url_for("login"))

        practice_stats = get_practice_stats(cursor, student_id)
        sutras_mastered = practice_stats["sutras_mastered"]
        overall_progress = round((sutras_mastered / TOTAL_SUTRAS) * 100, 1) if TOTAL_SUTRAS else 0

        milestones = [
            {"percent": 25, "title": "Bronze Achiever", "icon": "🥉"},
            {"percent": 50, "title": "Silver Achiever", "icon": "🥈"},
            {"percent": 75, "title": "Gold Achiever", "icon": "🥇"},
            {"percent": 100, "title": "Vedic Math Master", "icon": "🏆"},
        ]

        for m in milestones:
            m["unlocked"] = overall_progress >= m["percent"]

        return render_template(
            "certificates.html",
            student=student,
            milestones=milestones,
            overall_progress=overall_progress,
            sutras_mastered=sutras_mastered
        )

    except Exception as e:
        print("CERTIFICATES ERROR:", e)
        return "Certificates Error", 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )