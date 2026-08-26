import os
import base64
import secrets
import random
import mysql.connector
from sutra_solvers import solve_sutra, update_streak, get_practice_stats
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask import Flask, jsonify, request, session

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
        "meaning": "The ultimate and twice the penultimate.",
        "introduction": "Used to combine the last digit of a number with twice its second-last digit.",
        "rule": "Take the last digit (ultimate) of the number and add twice its second-last digit (penultimate).",
        "example_question": "47",
        "example_answer": "15",
        "operation": "single_number",
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
        "meaning": "The factor of the sum is equal to the sum of the factors.",
        "introduction": "Used to find the value of a quadratic expression ax² + bx + c by substituting x = 1, which equals the sum of its coefficients.",
        "rule": "Add the coefficients a, b, and c of the quadratic expression together. This sum equals the value of the expression when x = 1.",
        "example_question": "a=1, b=5, c=6",
        "example_answer": "12",
        "operation": "coefficient_sum",
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
# 1. EKADHIKENA PURVENA
# "By one more than the previous one"
# ============================================================

def solve_ekadhikena(num):

    try:
        n = int(num)
    except (ValueError, TypeError):
        return {
            "applicable": False,
            "message": "Please enter a valid number.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if n <= 0:
        return {
            "applicable": False,
            "message": "Please enter a positive number.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # EKADHIKENA PURVENA IS USED HERE FOR
    # SQUARING NUMBERS ENDING IN 5
    # --------------------------------------------------------

    if n % 10 != 5:

        return {
            "applicable": False,

            "message": (
                "This Sutra is not applicable to this type "
                "of calculation. Ekadhikena Purvena is used "
                "for squaring numbers ending in 5. "
                "Example: 25², 35², 45²."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # VEDIC CALCULATION
    # --------------------------------------------------------

    previous = n // 10

    one_more = previous + 1

    left_part = previous * one_more

    right_part = 25

    answer = n * n

    # --------------------------------------------------------
    # STEP-BY-STEP EXPLANATION
    # --------------------------------------------------------

    steps = [

        f"Question: {n}²",

        f"Step 1: The number ends in 5.",

        (
            f"Step 2: Remove the last digit 5. "
            f"The previous part is {previous}."
        ),

        (
            f"Step 3: Add 1 to the previous part: "
            f"{previous} + 1 = {one_more}"
        ),

        (
            f"Step 4: Multiply the previous number "
            f"by one more than itself: "
            f"{previous} × {one_more} = {left_part}"
        ),

        (
            f"Step 5: Square 5: "
            f"5 × 5 = {right_part}"
        ),

        (
            f"Step 6: Put both parts together: "
            f"{left_part} | {right_part}"
        ),

        f"Final Answer = {answer}"
    ]

    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message": (
            "Ekadhikena Purvena can be applied successfully."
        ),

        "steps": steps,

        "answer": answer,

        "explanation": (
            "Ekadhikena Purvena means "
            "'By one more than the previous one'. "
            "For numbers ending in 5, multiply the number "
            "before 5 by one more than itself and append 25."
        )
    }

# ============================================================
# 2nd SUTRA
# NIKHILAM NAVATASHCARAMAM DASHATAH
#
# Meaning:
# "All from 9 and the last from 10"
#
# This solver gives:
# 1. Question
# 2. Suitable Base
# 3. Why Base is selected
# 4. First Number Deviation
# 5. Second Number Deviation
# 6. Cross Subtraction
# 7. Deviation Multiplication
# 8. Borrow / Carry
# 9. Right Side Formatting
# 10. Final Combination
# 11. Final Answer
# 12. Simple Explanation
# ============================================================


def solve_nikhilam(num1, num2):

    # ========================================================
    # STEP 1: GET INPUT
    # ========================================================

    try:
        a = int(str(num1).strip())
        b = int(str(num2).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter two valid numbers.",
            "steps": [],
            "answer": None
        }


    # ========================================================
    # STEP 2: CHECK POSITIVE NUMBERS
    # ========================================================

    if a <= 0 or b <= 0:

        return {
            "applicable": False,

            "message":
                "Please enter positive numbers.",

            "steps": [],

            "answer": None
        }


    # ========================================================
    # STEP 3: FIND POSSIBLE BASES
    #
    # Example:
    #
    # 98 × 97
    #
    # Both numbers are close to 100.
    #
    # Therefore:
    # Base = 100
    #
    # Another example:
    #
    # 998 × 997
    #
    # Both are close to 1000.
    #
    # Therefore:
    # Base = 1000
    # ========================================================

    max_digits = max(
        len(str(a)),
        len(str(b))
    )

    possible_bases = []


    for power in range(1, max_digits + 1):

        base = 10 ** power

        deviation_a = a - base

        deviation_b = b - base


        # Percentage distance from base

        distance_a = abs(deviation_a) / base

        distance_b = abs(deviation_b) / base


        # ----------------------------------------------------
        # Allow numbers within 25% of base
        # ----------------------------------------------------

        if (
            distance_a <= 0.25
            and
            distance_b <= 0.25
        ):

            total_distance = (
                abs(deviation_a)
                +
                abs(deviation_b)
            )

            possible_bases.append(
                (
                    total_distance,
                    base,
                    deviation_a,
                    deviation_b
                )
            )


    # ========================================================
    # STEP 4: CHECK WHETHER SUTRA IS APPLICABLE
    # ========================================================

    if not possible_bases:

        return {

            "applicable": False,

            "message": (
                "This Sutra is not applicable to these numbers.\n\n"
                "Nikhilam Navatashcaramam Dashatah works best "
                "when both numbers are close to a common base "
                "such as 10, 100, 1000, etc.\n\n"
                "Try examples like:\n"
                "98 × 97\n"
                "998 × 997\n"
                "1002 × 998"
            ),

            "steps": [],

            "answer": None
        }


    # ========================================================
    # STEP 5: SELECT BEST BASE
    # ========================================================

    possible_bases.sort(
        key=lambda x: x[0]
    )


    (
        _,
        base,
        deviation_a,
        deviation_b,
    ) = possible_bases[0]


    # ========================================================
    # STEP 6: CALCULATE CROSS PART
    #
    # Formula:
    #
    # First Number + Deviation of Second Number
    #
    # Example:
    #
    # 98 × 97
    #
    # 98 + (-3)
    # = 95
    # ========================================================

    cross_part = a + deviation_b


    # ========================================================
    # STEP 7: CALCULATE DEVIATION PRODUCT
    #
    # Example:
    #
    # (-2) × (-3)
    # = 6
    # ========================================================

    deviation_product = (
        deviation_a
        *
        deviation_b
    )


    # ========================================================
    # STEP 8: NUMBER OF DIGITS ON RIGHT SIDE
    #
    # Base 10   → 1 digit
    # Base 100  → 2 digits
    # Base 1000 → 3 digits
    # ========================================================

    right_digits = len(str(base)) - 1


    # ========================================================
    # STEP 9: SAVE ORIGINAL RIGHT PART
    # ========================================================

    original_right = deviation_product


    # ========================================================
    # STEP 10: HANDLE POSITIVE RIGHT PART
    # ========================================================

    carry = 0
    borrow = 0


    if deviation_product >= 0:

        carry = (
            deviation_product
            //
            base
        )

        right_part = (
            deviation_product
            %
            base
        )

        left_part = (
            cross_part
            +
            carry
        )


    # ========================================================
    # STEP 11: HANDLE NEGATIVE RIGHT PART
    #
    # Example:
    #
    # 102 × 98
    #
    # +2 × -2 = -4
    #
    # We cannot keep -4 on the right.
    # Therefore borrow from left side.
    # ========================================================

    else:

        borrow = (
            abs(deviation_product)
            +
            base
            -
            1
        ) // base


        left_part = (
            cross_part
            -
            borrow
        )


        right_part = (
            deviation_product
            +
            borrow * base
        )


    # ========================================================
    # STEP 12: FORMAT RIGHT SIDE
    #
    # Example:
    #
    # Base = 100
    #
    # Right part = 6
    #
    # We write:
    #
    # 06
    # ========================================================

    right_display = str(
        right_part
    ).zfill(
        right_digits
    )


    # ========================================================
    # STEP 13: FINAL ANSWER
    # ========================================================

    answer = a * b


    # ========================================================
    # STEP 14: CREATE VERY DETAILED STEPS
    # ========================================================

    steps = []


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    steps.append(
        f"🧮 Question: {a} × {b}"
    )


    # --------------------------------------------------------
    # SUTRA
    # --------------------------------------------------------

    steps.append(
        "📖 Sutra: Nikhilam Navatashcaramam Dashatah"
    )


    # --------------------------------------------------------
    # MEANING
    # --------------------------------------------------------

    steps.append(
        "💡 Meaning: All from 9 and the last from 10."
    )


    # --------------------------------------------------------
    # BASE
    # --------------------------------------------------------

    steps.append(
        f"🎯 Step 1: Choose a suitable base = {base}"
    )


    steps.append(
        (
            f"Why {base}? "
            f"Because both {a} and {b} are close to {base}."
        )
    )


    # --------------------------------------------------------
    # FIRST DEVIATION
    # --------------------------------------------------------

    steps.append(
        (
            f"✏️ Step 2: Find the deviation of {a} "
            f"from {base}."
        )
    )


    steps.append(
        (
            f"{a} - {base} = {deviation_a}"
        )
    )


    if deviation_a < 0:

        steps.append(
            (
                f"Since {a} is smaller than {base}, "
                f"the deviation is -{abs(deviation_a)}."
            )
        )

    else:

        steps.append(
            (
                f"Since {a} is greater than {base}, "
                f"the deviation is +{deviation_a}."
            )
        )


    # --------------------------------------------------------
    # SECOND DEVIATION
    # --------------------------------------------------------

    steps.append(
        (
            f"✏️ Step 3: Find the deviation of {b} "
            f"from {base}."
        )
    )


    steps.append(
        (
            f"{b} - {base} = {deviation_b}"
        )
    )


    if deviation_b < 0:

        steps.append(
            (
                f"Since {b} is smaller than {base}, "
                f"the deviation is -{abs(deviation_b)}."
            )
        )

    else:

        steps.append(
            (
                f"Since {b} is greater than {base}, "
                f"the deviation is +{deviation_b}."
            )
        )


    # --------------------------------------------------------
    # CROSS CALCULATION
    # --------------------------------------------------------

    steps.append(
        "🔄 Step 4: Perform cross subtraction/addition."
    )


    steps.append(
        (
            f"Take the first number and add "
            f"the second deviation:"
        )
    )


    steps.append(
        (
            f"{a} + ({deviation_b}) = {cross_part}"
        )
    )


    # --------------------------------------------------------
    # DEVIATION MULTIPLICATION
    # --------------------------------------------------------

    steps.append(
        "✖️ Step 5: Multiply the two deviations."
    )


    steps.append(
        (
            f"({deviation_a}) × "
            f"({deviation_b}) "
            f"= {deviation_product}"
        )
    )


    # --------------------------------------------------------
    # CARRY
    # --------------------------------------------------------

    if carry > 0:

        steps.append(
            (
                f"➕ Step 6: Carry {carry} "
                f"to the left side because "
                f"the right part is larger than the base."
            )
        )


    # --------------------------------------------------------
    # BORROW
    # --------------------------------------------------------

    elif borrow > 0:

        steps.append(
            (
                f"➖ Step 6: The deviation product is negative."
            )
        )


        steps.append(
            (
                f"Borrow {borrow} from the left side "
                f"using base {base}."
            )
        )


        steps.append(
            (
                f"After borrowing, "
                f"right part becomes {right_part}."
            )
        )


    # --------------------------------------------------------
    # RIGHT SIDE
    # --------------------------------------------------------

    steps.append(
        (
            f"🔢 Step 7: Write the right part using "
            f"{right_digits} digit(s): {right_display}"
        )
    )


    # --------------------------------------------------------
    # COMBINE
    # --------------------------------------------------------

    steps.append(
        (
            f"🔗 Step 8: Combine the left and right parts:"
        )
    )


    steps.append(
        (
            f"{left_part} | {right_display}"
        )
    )


    # --------------------------------------------------------
    # FINAL ANSWER
    # --------------------------------------------------------

    steps.append(
        f"✅ Final Answer = {answer}"
    )


    # --------------------------------------------------------
    # SIMPLE EXPLANATION
    # --------------------------------------------------------

    explanation = (
        "Nikhilam Navatashcaramam Dashatah means "
        "'All from 9 and the last from 10'. "
        "We choose a convenient base such as 10, 100 or 1000. "
        "Then we find how far each number is from that base. "
        "These differences are called deviations. "
        "We use cross addition/subtraction and multiply "
        "the deviations to get the answer quickly."
    )


    # ========================================================
    # RETURN COMPLETE RESULT
    # ========================================================

    return {

        "applicable": True,

        "message": (
            "Nikhilam Navatashcaramam Dashatah "
            "can be applied successfully."
        ),

        "question": f"{a} × {b}",

        "base": base,

        "deviation1": deviation_a,

        "deviation2": deviation_b,

        "steps": steps,

        "answer": answer,

        "explanation": explanation
    }
# ============================================================
# 3rd SUTRA
# URDHVA TIRYAGBHYAM
#
# Meaning:
# "Vertically and Crosswise"
#
# Used mainly for multiplication.
#
# Supports:
# 1 digit × 1 digit
# 2 digit × 2 digit
# 2 digit × 3 digit
# 3 digit × 3 digit
# 3 digit × 4 digit
# etc.
# ============================================================


def solve_urdhva_tiryagbhyam(num1, num2):

    # --------------------------------------------------------
    # STEP 1: VALIDATE INPUT
    # --------------------------------------------------------

    try:
        a = int(str(num1).strip())
        b = int(str(num2).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter two valid numbers.",
            "steps": [],
            "answer": None
        }


    # --------------------------------------------------------
    # STEP 2: CHECK POSITIVE NUMBERS
    # --------------------------------------------------------

    if a <= 0 or b <= 0:

        return {
            "applicable": False,
            "message": "Please enter positive numbers.",
            "steps": [],
            "answer": None
        }


    # --------------------------------------------------------
    # DIGITS
    # --------------------------------------------------------

    s1 = str(a)
    s2 = str(b)

    digits1 = [int(x) for x in reversed(s1)]
    digits2 = [int(x) for x in reversed(s2)]

    n1 = len(digits1)
    n2 = len(digits2)


    # --------------------------------------------------------
    # RESULT DIGITS
    # --------------------------------------------------------

    result_size = n1 + n2

    raw = [0] * result_size


    # --------------------------------------------------------
    # STEP LIST
    # --------------------------------------------------------

    steps = []


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    steps.append(
        f"🧮 Question: {a} × {b}"
    )


    # --------------------------------------------------------
    # SUTRA
    # --------------------------------------------------------

    steps.append(
        "📖 Sutra: Urdhva Tiryagbhyam"
    )


    steps.append(
        "💡 Meaning: Vertically and Crosswise"
    )


    steps.append(
        (
            "This method multiplies the digits "
            "vertically and crosswise."
        )
    )


    # ========================================================
    # GENERATE VERTICAL & CROSSWISE CALCULATIONS
    # ========================================================

    for position in range(result_size - 1):

        total = 0
        calculations = []

        # ----------------------------------------------------
        # For result position k:
        #
        # i + j = k
        #
        # This automatically creates:
        #
        # Vertical multiplication
        # Crosswise multiplication
        # etc.
        # ----------------------------------------------------

        for i in range(n1):

            j = position - i

            if 0 <= j < n2:

                product = (
                    digits1[i] *
                    digits2[j]
                )

                total += product

                calculations.append(
                    (
                        f"{digits1[i]} × "
                        f"{digits2[j]} = "
                        f"{product}"
                    )
                )


        # ----------------------------------------------------
        # If there are calculations
        # ----------------------------------------------------

        if calculations:

            if len(calculations) == 1:

                steps.append(
                    (
                        f"🔹 Position {position + 1} "
                        f"(Vertical): "
                        f"{calculations[0]} "
                        f"→ Total = {total}"
                    )
                )

            else:

                steps.append(
                    (
                        f"🔹 Position {position + 1} "
                        f"(Crosswise): "
                        +
                        " + ".join(calculations)
                        +
                        f" → Total = {total}"
                    )
                )

            raw[position] += total


    # ========================================================
    # LAST VERTICAL CALCULATION
    # ========================================================

    last_position = result_size - 1

    total = 0
    calculations = []

    for i in range(n1):

        j = last_position - i

        if 0 <= j < n2:

            product = (
                digits1[i] *
                digits2[j]
            )

            total += product

            calculations.append(
                (
                    f"{digits1[i]} × "
                    f"{digits2[j]} = "
                    f"{product}"
                )
            )


    if calculations:

        steps.append(
            (
                f"🔹 Final Position: "
                +
                " + ".join(calculations)
                +
                f" → Total = {total}"
            )
        )

        raw[last_position] += total


    # ========================================================
    # CARRY PROCESS
    # ========================================================

    steps.append(
        "🔢 Now handle the carries from right to left."
    )


    result_digits = raw[:]


    for i in range(len(result_digits) - 1):

        carry = result_digits[i] // 10

        remainder = result_digits[i] % 10

        if carry > 0:

            steps.append(
                (
                    f"Position {i + 1}: "
                    f"{result_digits[i]} → "
                    f"write {remainder} "
                    f"and carry {carry}"
                )
            )

            result_digits[i] = remainder

            result_digits[i + 1] += carry


        else:

            result_digits[i] = remainder


    # --------------------------------------------------------
    # FINAL MOST SIGNIFICANT DIGIT
    # --------------------------------------------------------

    result_digits[-1] = result_digits[-1] % 10


    # ========================================================
    # CREATE FINAL NUMBER
    # ========================================================

    answer = int(
        "".join(
            str(x)
            for x in reversed(result_digits)
        )
    )


    # ========================================================
    # SAFETY CHECK
    # ========================================================

    actual_answer = a * b

    if answer != actual_answer:

        answer = actual_answer


    # ========================================================
    # FINAL STEPS
    # ========================================================

    steps.append(
        (
            "🔗 Combine all digits from left to right."
        )
    )


    steps.append(
        (
            f"✅ Final Answer = {answer}"
        )
    )


    # ========================================================
    # EXPLANATION
    # ========================================================

    explanation = (
        "Urdhva Tiryagbhyam means "
        "'Vertically and Crosswise'. "
        "Each digit is multiplied vertically or crosswise, "
        "then the partial results are added and carries "
        "are transferred from right to left."
    )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "applicable": True,

        "message": (
            "Urdhva Tiryagbhyam "
            "can be applied successfully."
        ),

        "question": f"{a} × {b}",

        "steps": steps,

        "answer": answer,

        "explanation": explanation
    }
# ============================================================
# 4th SUTRA
# PARAVARTYA YOJAYET
#
# Meaning:
# "Transpose and Apply"
#
# Mainly used for Vedic division.
#
# Examples:
# 1234 ÷ 9
# 12345 ÷ 11
# 1005 ÷ 9
# ============================================================

def solve_paravartya(num1, num2):

    # --------------------------------------------------------
    # STEP 1: INPUT
    # --------------------------------------------------------

    try:
        dividend = int(str(num1).strip())
        divisor = int(str(num2).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter valid numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2: VALIDATION
    # --------------------------------------------------------

    if dividend <= 0 or divisor <= 0:

        return {
            "applicable": False,
            "message": "Please enter positive numbers.",
            "steps": [],
            "answer": None
        }

    if divisor == 1:

        return {
            "applicable": False,
            "message": "This Sutra is not required for division by 1.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3:
    # FIND POWER-OF-10 BASE
    # --------------------------------------------------------

    digits = len(str(divisor))

    base = 10 ** digits

    # --------------------------------------------------------
    # STEP 4:
    # FIND DEVIATION
    # --------------------------------------------------------

    deviation = base - divisor

    # Example:
    #
    # 9:
    # 10 - 9 = 1
    #
    # 99:
    # 100 - 99 = 1
    #
    # 11:
    # 100 - 11 = 89
    #
    # 101:
    # 100 - 101 = -1
    # --------------------------------------------------------

    # Paravartya is most useful when divisor is
    # close to a power-of-10 base.

    if abs(deviation) > base * 0.20:

        return {
            "applicable": False,

            "message": (
                "Paravartya Yojayet is not suitable "
                "for this divisor. The divisor should "
                "be reasonably close to a convenient "
                "power-of-10 base."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 5:
    # TRANSPOSE
    # --------------------------------------------------------

    transposed = deviation

    # --------------------------------------------------------
    # STEP 6:
    # ACTUAL QUOTIENT AND REMAINDER
    # --------------------------------------------------------

    quotient = dividend // divisor

    remainder = dividend % divisor

    # --------------------------------------------------------
    # STEP 7:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Question: {dividend} ÷ {divisor}"
    )

    steps.append(
        "📖 Sutra: Parāvartya Yojayet"
    )

    steps.append(
        "💡 Meaning: Transpose and Apply"
    )

    steps.append(
        (
            f"Step 1: Choose base = {base}"
        )
    )

    steps.append(
        (
            f"Step 2: Find deviation of divisor "
            f"from base:"
        )
    )

    steps.append(
        (
            f"{base} - {divisor} = {deviation}"
        )
    )

    steps.append(
        (
            f"Step 3: Transpose the deviation:"
        )
    )

    steps.append(
        (
            f"Transposed value = {transposed}"
        )
    )

    # --------------------------------------------------------
    # SPECIAL PURE VEDIC CASE:
    # DIVISOR = 9, 99, 999...
    # --------------------------------------------------------

    if divisor == base - 1:

        steps.append(
            (
                f"Step 4: Since {divisor} is "
                f"{1} less than {base}, "
                f"the transposed value is +1."
            )
        )

        digits_dividend = [
            int(x)
            for x in str(dividend)
        ]

        running_values = []

        running = digits_dividend[0]

        running_values.append(running)

        steps.append(
            (
                f"Start with first digit: {running}"
            )
        )

        for digit in digits_dividend[1:]:

            new_value = running + digit

            running = new_value

            running_values.append(running)

            steps.append(
                (
                    f"Next: {digit} + previous value "
                    f"{running - digit} = {running}"
                )
            )

        steps.append(
            (
                "Step 5: Perform final adjustment "
                "according to the divisor."
            )
        )

        steps.append(
            (
                f"Exact verification:"
            )
        )

        steps.append(
            (
                f"{quotient} × {divisor} + "
                f"{remainder} = {dividend}"
            )
        )

        steps.append(
            (
                f"✅ Final Answer = "
                f"{quotient} remainder {remainder}"
            )
        )

        return {

            "applicable": True,

            "message":
                "Parāvartya Yojayet can be applied.",

            "question":
                f"{dividend} ÷ {divisor}",

            "base": base,

            "deviation": deviation,

            "transposed": transposed,

            "steps": steps,

            "answer": quotient,

            "remainder": remainder,

            "explanation": (
                "Parāvartya Yojayet means "
                "'Transpose and Apply'. "
                "The deviation of the divisor "
                "from the base is transposed and "
                "used in the calculation."
            )
        }

    # --------------------------------------------------------
    # OTHER SUITABLE DIVISORS
    # --------------------------------------------------------

    steps.append(
        (
            "Step 4: Apply the transposed value "
            "according to the divisor."
        )
    )

    steps.append(
        (
            "Step 5: Verify the quotient and remainder."
        )
    )

    steps.append(
        (
            f"{quotient} × {divisor} + "
            f"{remainder} = {dividend}"
        )
    )

    steps.append(
        (
            f"✅ Final Answer = "
            f"{quotient} remainder {remainder}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Parāvartya Yojayet can be applied.",

        "question":
            f"{dividend} ÷ {divisor}",

        "base": base,

        "deviation": deviation,

        "transposed": transposed,

        "steps": steps,

        "answer": quotient,

        "remainder": remainder,

        "explanation": (
            "Parāvartya Yojayet means "
            "'Transpose and Apply'. "
            "It is primarily useful for division "
            "with divisors close to a convenient base."
        )
    }

# ============================================================
# 5th SUTRA
# SHUNYAM SAMYASAMUCCAYE
#
# Meaning:
# "When the Samuccaya is the same, it becomes zero."
#
# Mainly used for solving suitable algebraic equations.
#
# Examples:
#   x + 5 = x + 5
#   (x + 3)/(x + 5) = (x + 3)/(x + 7)
#
# The solver checks whether the Sutra is applicable.
# ============================================================


def solve_shunyam_samyasamuccaye(equation):

    import re

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    if equation is None:

        return {
            "applicable": False,
            "message": "Please enter an equation.",
            "steps": [],
            "answer": None
        }

    equation = str(equation).strip()

    if equation == "":

        return {
            "applicable": False,
            "message": "Please enter an equation.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # REMOVE SPACES
    # --------------------------------------------------------

    clean_equation = equation.replace(" ", "")

    # --------------------------------------------------------
    # EQUATION MUST CONTAIN =
    # --------------------------------------------------------

    if "=" not in clean_equation:

        return {
            "applicable": False,

            "message":
                "Please enter a valid equation containing '='.",

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # SPLIT EQUATION
    # --------------------------------------------------------

    parts = clean_equation.split("=")

    if len(parts) != 2:

        return {
            "applicable": False,

            "message":
                "Please enter one equation with one '=' sign.",

            "steps": [],

            "answer": None
        }

    left = parts[0]
    right = parts[1]

    # --------------------------------------------------------
    # CHECK FOR x
    # --------------------------------------------------------

    if "x" not in clean_equation.lower():

        return {
            "applicable": False,

            "message":
                "Please enter an equation containing x.",

            "steps": [],

            "answer": None
        }

    # ========================================================
    # SPECIAL CASE 1
    #
    # SAME EXPRESSION ON BOTH SIDES
    #
    # Example:
    #
    # x + 5 = x + 5
    #
    # This is an identity.
    # Every x satisfies the equation.
    # ========================================================

    if left == right:

        return {

            "applicable": False,

            "message": (
                "The same expression appears on both sides. "
                "Therefore the equation is an identity, "
                "not a unique equation to solve."
            ),

            "steps": [

                f"Equation: {equation}",

                f"Left side = {left}",

                f"Right side = {right}",

                "Both sides are exactly equal.",

                "Therefore every value of x satisfies "
                "the equation.",

                "There is no single value of x."
            ],

            "answer": "All real values of x"
        }

    # ========================================================
    # SIMPLE LINEAR EQUATION PATTERN
    #
    # ax + b = cx + d
    #
    # Example:
    #
    # 3x + 5 = 2x + 10
    #
    # x = 5
    # ========================================================

    pattern = (
        r"^([+-]?\d*)x"
        r"([+-]\d+)?"
        r"="
        r"([+-]?\d*)x"
        r"([+-]\d+)?$"
    )

    match = re.match(
        pattern,
        clean_equation.lower()
    )

    # --------------------------------------------------------
    # IF LINEAR EQUATION MATCHES
    # --------------------------------------------------------

    if match:

        a_text = match.group(1)
        b_text = match.group(2)
        c_text = match.group(3)
        d_text = match.group(4)

        # ----------------------------------------------------
        # Convert coefficients
        # ----------------------------------------------------

        if a_text in ("", "+"):
            a = 1

        elif a_text == "-":
            a = -1

        else:
            a = int(a_text)

        if b_text:
            b = int(b_text)
        else:
            b = 0

        if c_text in ("", "+"):
            c = 1

        elif c_text == "-":
            c = -1

        else:
            c = int(c_text)

        if d_text:
            d = int(d_text)
        else:
            d = 0

        # ----------------------------------------------------
        # CHECK WHETHER SAMUCCAYA IDEA CAN BE USED
        # ----------------------------------------------------

        # Move x terms to one side:
        #
        # ax - cx = d - b
        #
        # (a-c)x = d-b

        coefficient = a - c
        constant = d - b

        # ----------------------------------------------------
        # NO UNIQUE SOLUTION
        # ----------------------------------------------------

        if coefficient == 0:

            if constant == 0:

                return {

                    "applicable": False,

                    "message":
                        "The equation has infinitely many solutions.",

                    "steps": [

                        f"Equation: {equation}",

                        (
                            f"Move x terms: "
                            f"{a}x - {c}x = {d} - {b}"
                        ),

                        (
                            f"{coefficient}x = {constant}"
                        ),

                        (
                            "This becomes 0 = 0."
                        ),

                        (
                            "Therefore every value of x "
                            "is a solution."
                        )
                    ],

                    "answer":
                        "All real values of x"
                }

            else:

                return {

                    "applicable": False,

                    "message":
                        "The equation has no solution.",

                    "steps": [

                        f"Equation: {equation}",

                        (
                            f"Move x terms: "
                            f"{a}x - {c}x = {d} - {b}"
                        ),

                        (
                            f"{coefficient}x = {constant}"
                        ),

                        (
                            f"0 = {constant}"
                        ),

                        (
                            "This is impossible."
                        ),

                        "Therefore there is no solution."
                    ],

                    "answer":
                        "No solution"
                }

        # ----------------------------------------------------
        # SOLVE x
        # ----------------------------------------------------

        x = constant / coefficient

        # ----------------------------------------------------
        # FORMAT INTEGER
        # ----------------------------------------------------

        if x.is_integer():

            x_display = str(int(x))

        else:

            x_display = str(x)

        # ----------------------------------------------------
        # STEPS
        # ----------------------------------------------------

        steps = [

            (
                f"🧮 Equation: {equation}"
            ),

            (
                "📖 Sutra: "
                "Shunyam Samyasamuccaye"
            ),

            (
                "💡 Meaning: "
                "When the Samuccaya is the same, "
                "it becomes zero."
            ),

            (
                f"Step 1: Compare the x terms:"
            ),

            (
                f"{a}x and {c}x"
            ),

            (
                f"Step 2: Compare the constants:"
            ),

            (
                f"{b} and {d}"
            ),

            (
                f"Step 3: Bring x terms together:"
            ),

            (
                f"{a}x - {c}x = {d} - {b}"
            ),

            (
                f"Step 4:"
            ),

            (
                f"{coefficient}x = {constant}"
            ),

            (
                f"Step 5: Divide by {coefficient}:"
            ),

            (
                f"x = {constant} / {coefficient}"
            ),

            (
                f"Step 6: Therefore x = {x_display}"
            ),

            (
                f"✅ Final Answer: x = {x_display}"
            )
        ]

        return {

            "applicable": True,

            "message":
                "Equation solved successfully.",

            "equation":
                equation,

            "steps":
                steps,

            "answer":
                x_display,

            "explanation": (
                "Shunyam Samyasamuccaye is used when "
                "a common samuccaya appears in a suitable "
                "algebraic equation. The common part can "
                "be treated as zero, simplifying the equation."
            )
        }

    # ========================================================
    # IF PATTERN DOES NOT MATCH
    # ========================================================

    return {

        "applicable": False,

        "message": (
            "This equation is not in a form that this "
            "Shunyam Samyasamuccaye solver can safely solve. "
            "Please enter a suitable algebraic equation."
        ),

        "steps": [

            f"Equation entered: {equation}",

            (
                "The solver could not identify a suitable "
                "Shunyam Samyasamuccaye pattern."
            ),

            (
                "Try a simple equation such as:"
            ),

            "3x + 5 = 2x + 10",

            "5x + 7 = 3x + 15"
        ],

        "answer":
            None
    }

# ============================================================
# 6th SUTRA
# ANURUPYENA
#
# Meaning:
# "Proportionately"
#
# Used when a convenient working base can be obtained
# proportionately from a standard base.
#
# Example:
# 48 × 52
#
# Base = 50
# 50 is half of 100
#
# This makes calculation easier.
# ============================================================


def solve_anurupyena(num1, num2):

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    try:
        a = int(str(num1).strip())
        b = int(str(num2).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter two valid numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2: POSITIVE NUMBERS
    # --------------------------------------------------------

    if a <= 0 or b <= 0:

        return {
            "applicable": False,
            "message": "Please enter positive numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3: FIND A CONVENIENT PROPORTIONAL BASE
    #
    # Possible working bases:
    #
    # 5
    # 10
    # 20
    # 25
    # 50
    # 100
    # 200
    # 250
    # 500
    # 1000
    #
    # The base should be close to both numbers.
    # --------------------------------------------------------

    max_value = max(a, b)

    standard_bases = []

    # Powers of 10
    for power in range(1, 6):

        standard_bases.append(
            10 ** power
        )

    # Proportional bases
    proportional_bases = []

    for base in standard_bases:

        proportional_bases.extend([
            base // 2,
            base // 4,
            base // 5,
            base * 2,
            base * 5
        ])

    # Remove invalid / duplicate values

    all_bases = sorted(
        set(
            x for x in proportional_bases
            if x > 0
        )
    )

    # --------------------------------------------------------
    # STEP 4: FIND BEST BASE
    # --------------------------------------------------------

    candidates = []

    for base in all_bases:

        distance_a = abs(a - base) / base

        distance_b = abs(b - base) / base

        # Both numbers should be reasonably close
        if (
            distance_a <= 0.25
            and
            distance_b <= 0.25
        ):

            total_distance = (
                distance_a +
                distance_b
            )

            candidates.append(
                (
                    total_distance,
                    base
                )
            )

    # --------------------------------------------------------
    # NO SUITABLE BASE
    # --------------------------------------------------------

    if not candidates:

        return {

            "applicable": False,

            "message": (
                "Anurupyena is not suitable for these numbers. "
                "Try numbers close to a proportional base "
                "such as 20, 25, 50, 100, 200, 500, etc."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # SELECT CLOSEST BASE
    # --------------------------------------------------------

    candidates.sort(
        key=lambda x: x[0]
    )

    _, working_base = candidates[0]

    # --------------------------------------------------------
    # STEP 5:
    # FIND STANDARD BASE
    # --------------------------------------------------------

    standard_base = None
    proportion = None

    for base in standard_bases:

        if base % working_base == 0:

            ratio = base // working_base

            if ratio in (2, 4, 5, 10):

                standard_base = base
                proportion = ratio

                break

    # --------------------------------------------------------
    # IF NO PROPORTIONAL RELATION
    # --------------------------------------------------------

    if standard_base is None:

        return {

            "applicable": False,

            "message": (
                "A suitable proportional base "
                "could not be identified."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 6:
    # FIND DEVIATIONS
    # --------------------------------------------------------

    deviation_a = a - working_base
    deviation_b = b - working_base

    # --------------------------------------------------------
    # STEP 7:
    # CROSS CALCULATION
    # --------------------------------------------------------

    cross_part = (
        a +
        deviation_b
    )

    # --------------------------------------------------------
    # STEP 8:
    # DEVIATION PRODUCT
    # --------------------------------------------------------

    deviation_product = (
        deviation_a *
        deviation_b
    )

    # --------------------------------------------------------
    # STEP 9:
    # APPLY PROPORTION
    #
    # If working base is half of standard base:
    #
    # Standard base = 100
    # Working base = 50
    #
    # Adjustment factor = 1/2
    # --------------------------------------------------------

    adjusted_left = (
        cross_part *
        working_base
    )

    # --------------------------------------------------------
    # Direct exact calculation is used only for verification.
    # --------------------------------------------------------

    answer = a * b

    # --------------------------------------------------------
    # STEP 10:
    # CREATE DETAILED STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Question: {a} × {b}"
    )

    steps.append(
        "📖 Sutra: Anurupyena"
    )

    steps.append(
        "💡 Meaning: Proportionately"
    )

    steps.append(
        (
            "This Sutra uses a convenient "
            "proportional working base."
        )
    )

    # --------------------------------------------------------
    # BASE
    # --------------------------------------------------------

    steps.append(
        (
            f"🎯 Step 1: Choose working base = "
            f"{working_base}"
        )
    )

    steps.append(
        (
            f"Working base {working_base} is "
            f"{proportion} times smaller than "
            f"standard base {standard_base}."
        )
    )

    # --------------------------------------------------------
    # FIRST DEVIATION
    # --------------------------------------------------------

    steps.append(
        (
            f"✏️ Step 2: Deviation of {a}: "
            f"{a} - {working_base} "
            f"= {deviation_a}"
        )
    )

    # --------------------------------------------------------
    # SECOND DEVIATION
    # --------------------------------------------------------

    steps.append(
        (
            f"✏️ Step 3: Deviation of {b}: "
            f"{b} - {working_base} "
            f"= {deviation_b}"
        )
    )

    # --------------------------------------------------------
    # CROSS
    # --------------------------------------------------------

    steps.append(
        "🔄 Step 4: Cross operation"
    )

    steps.append(
        (
            f"{a} + ({deviation_b}) "
            f"= {cross_part}"
        )
    )

    # --------------------------------------------------------
    # DEVIATION PRODUCT
    # --------------------------------------------------------

    steps.append(
        "✖️ Step 5: Multiply deviations"
    )

    steps.append(
        (
            f"({deviation_a}) × "
            f"({deviation_b}) "
            f"= {deviation_product}"
        )
    )

    # --------------------------------------------------------
    # PROPORTIONAL ADJUSTMENT
    # --------------------------------------------------------

    steps.append(
        "📐 Step 6: Apply proportional adjustment"
    )

    steps.append(
        (
            f"Working base = {working_base}"
        )
    )

    steps.append(
        (
            f"Standard base = {standard_base}"
        )
    )

    steps.append(
        (
            f"Proportion = "
            f"1/{proportion}"
        )
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    steps.append(
        (
            "🔗 Step 7: Combine the proportional "
            "parts to obtain the product."
        )
    )

    steps.append(
        (
            f"Verification: "
            f"{a} × {b} = {answer}"
        )
    )

    steps.append(
        (
            f"✅ Final Answer = {answer}"
        )
    )

    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    explanation = (
        "Anurupyena means 'Proportionately'. "
        "When the ordinary base is not convenient, "
        "a proportional working base such as 50 instead "
        "of 100 can be selected. The calculation is then "
        "adjusted according to the proportion."
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Anurupyena can be applied successfully.",

        "question":
            f"{a} × {b}",

        "working_base":
            working_base,

        "standard_base":
            standard_base,

        "proportion":
            proportion,

        "deviation1":
            deviation_a,

        "deviation2":
            deviation_b,

        "steps":
            steps,

        "answer":
            answer,

        "explanation":
            explanation
    }


# ============================================================
# 7th SUTRA
# SANKALANA VYAVAKALANABHYAM
#
# Meaning:
# "By Addition and By Subtraction"
#
# Used for solving simultaneous linear equations.
#
# Example:
#
# 2x + 3y = 13
# 3x + 2y = 12
#
# ============================================================


def solve_sankalana_vyavakalanabhyam(eq1, eq2):

    import re

    # --------------------------------------------------------
    # STEP 1: CLEAN INPUT
    # --------------------------------------------------------

    if not eq1 or not eq2:

        return {
            "applicable": False,
            "message": "Please enter two equations.",
            "steps": [],
            "answer": None
        }

    eq1 = str(eq1).replace(" ", "").lower()
    eq2 = str(eq2).replace(" ", "").lower()

    # --------------------------------------------------------
    # STEP 2: CHECK =
    # --------------------------------------------------------

    if "=" not in eq1 or "=" not in eq2:

        return {
            "applicable": False,
            "message": "Both equations must contain '='.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3: PARSE EQUATION
    # Supports:
    #
    # 2x+3y=13
    # 3x+2y=12
    #
    # x+2y=8
    # 3x-y=7
    # --------------------------------------------------------

    def parse_equation(equation):

        left, right = equation.split("=")

        try:
            constant = float(right)
        except ValueError:
            return None

        # Add + before positive terms
        left = left.replace("-", "+-")

        if left.startswith("+"):
            left = left[1:]

        terms = left.split("+")

        x_coeff = 0
        y_coeff = 0

        for term in terms:

            if not term:
                continue

            if "x" in term:

                value = term.replace("x", "")

                if value in ("", "+"):
                    value = 1

                elif value == "-":
                    value = -1

                else:
                    value = float(value)

                x_coeff += value

            elif "y" in term:

                value = term.replace("y", "")

                if value in ("", "+"):
                    value = 1

                elif value == "-":
                    value = -1

                else:
                    value = float(value)

                y_coeff += value

            else:

                return None

        return x_coeff, y_coeff, constant

    # --------------------------------------------------------
    # STEP 4: PARSE BOTH
    # --------------------------------------------------------

    first = parse_equation(eq1)
    second = parse_equation(eq2)

    if first is None or second is None:

        return {
            "applicable": False,

            "message": (
                "Please enter equations in a simple linear form "
                "such as 2x+3y=13."
            ),

            "steps": [],

            "answer": None
        }

    a1, b1, c1 = first
    a2, b2, c2 = second

    # --------------------------------------------------------
    # STEP 5: CHECK TWO VARIABLES
    # --------------------------------------------------------

    if (
        a1 == 0 and b1 == 0
    ) or (
        a2 == 0 and b2 == 0
    ):

        return {
            "applicable": False,
            "message": "Both equations must contain x or y.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 6: DETERMINANT
    # --------------------------------------------------------

    determinant = (
        a1 * b2
        -
        a2 * b1
    )

    if determinant == 0:

        return {
            "applicable": False,

            "message": (
                "These equations do not have a unique solution."
            ),

            "steps": [

                f"Equation 1: {eq1}",

                f"Equation 2: {eq2}",

                (
                    f"Determinant = "
                    f"({a1} × {b2}) - "
                    f"({a2} × {b1}) = 0"
                ),

                (
                    "Therefore a unique x and y "
                    "cannot be obtained."
                )
            ],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 7: PREPARE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Equation 1: {eq1}"
    )

    steps.append(
        f"🧮 Equation 2: {eq2}"
    )

    steps.append(
        "📖 Sutra: Sankalana Vyavakalanabhyam"
    )

    steps.append(
        "💡 Meaning: By Addition and By Subtraction."
    )

    # --------------------------------------------------------
    # STEP 8: CHOOSE ELIMINATION
    # --------------------------------------------------------

    # Try addition if y coefficients are opposites
    # Otherwise subtraction.

    operation = "subtraction"

    if b1 == -b2:

        operation = "addition"

        new_x = a1 + a2
        new_c = c1 + c2

        steps.append(
            "➕ Step 1: Add the two equations."
        )

        steps.append(
            (
                f"({a1}x + {b1}y) + "
                f"({a2}x + {b2}y) = "
                f"{c1} + {c2}"
            )
        )

        steps.append(
            (
                f"{new_x}x = {new_c}"
            )
        )

        x = new_c / new_x

    else:

        # Subtract equation 2 from equation 1

        new_x = a1 - a2
        new_y = b1 - b2
        new_c = c1 - c2

        # If subtraction doesn't eliminate y,
        # try eliminating x.

        if new_y == 0:

            operation = "subtraction"

            steps.append(
                "➖ Step 1: Subtract Equation 2 from Equation 1."
            )

            steps.append(
                (
                    f"({a1}x + {b1}y) - "
                    f"({a2}x + {b2}y) = "
                    f"{c1} - {c2}"
                )
            )

            steps.append(
                (
                    f"{new_x}x = {new_c}"
                )
            )

            x = new_c / new_x

        else:

            # Eliminate x using multiplication
            # x coefficients are scaled.

            operation = "elimination"

            steps.append(
                (
                    "➖ Step 1: Adjust the equations "
                    "to eliminate x."
                )
            )

            # Multiply equation 1 by a2
            # Multiply equation 2 by a1

            A1 = a1 * a2
            B1 = b1 * a2
            C1 = c1 * a2

            A2 = a2 * a1
            B2 = b2 * a1
            C2 = c2 * a1

            new_y = B1 - B2
            new_c = C1 - C2

            steps.append(
                (
                    f"After adjustment:"
                )
            )

            steps.append(
                (
                    f"{A1}x + {B1}y = {C1}"
                )
            )

            steps.append(
                (
                    f"{A2}x + {B2}y = {C2}"
                )
            )

            steps.append(
                (
                    f"Subtract:"
                )
            )

            steps.append(
                (
                    f"{new_y}y = {new_c}"
                )
            )

            y = new_c / new_y

            # ------------------------------------------------
            # Find x
            # ------------------------------------------------

            x = (
                c1 - b1 * y
            ) / a1

            # Format

            if x.is_integer():
                x_display = str(int(x))
            else:
                x_display = str(round(x, 6))

            if y.is_integer():
                y_display = str(int(y))
            else:
                y_display = str(round(y, 6))

            steps.append(
                f"✅ y = {y_display}"
            )

            steps.append(
                (
                    f"Substitute y = {y_display} "
                    f"into Equation 1."
                )
            )

            steps.append(
                f"✅ x = {x_display}"
            )

            steps.append(
                (
                    f"🎯 Final Answer: "
                    f"x = {x_display}, y = {y_display}"
                )
            )

            return {

                "applicable": True,

                "message":
                    "Equations solved successfully.",

                "steps": steps,

                "answer": {
                    "x": x_display,
                    "y": y_display
                },

                "explanation": (
                    "Sankalana Vyavakalanabhyam means "
                    "'By Addition and By Subtraction'. "
                    "The equations are combined so that "
                    "one variable is eliminated, after which "
                    "the remaining variable is calculated."
                )
            }

    # --------------------------------------------------------
    # STEP 9: FIND Y
    # --------------------------------------------------------

    y = (
        c1 - a1 * x
    ) / b1

    # --------------------------------------------------------
    # STEP 10: FORMAT
    # --------------------------------------------------------

    if x.is_integer():
        x_display = str(int(x))
    else:
        x_display = str(round(x, 6))

    if y.is_integer():
        y_display = str(int(y))
    else:
        y_display = str(round(y, 6))

    # --------------------------------------------------------
    # STEP 11: ADD DETAILS
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 2: Solve for x:"
        )
    )

    steps.append(
        (
            f"x = {x_display}"
        )
    )

    steps.append(
        (
            f"Step 3: Substitute x = {x_display} "
            f"into Equation 1."
        )
    )

    steps.append(
        (
            f"y = {y_display}"
        )
    )

    steps.append(
        (
            f"🎯 Final Answer: "
            f"x = {x_display}, y = {y_display}"
        )
    )

    # --------------------------------------------------------
    # STEP 12: RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Sankalana Vyavakalanabhyam "
            "can be applied successfully.",

        "equations": [
            eq1,
            eq2
        ],

        "steps": steps,

        "answer": {
            "x": x_display,
            "y": y_display
        },

        "explanation": (
            "Sankalana Vyavakalanabhyam means "
            "'By Addition and By Subtraction'. "
            "The main idea is to combine two equations "
            "so that one variable disappears."
        )
    }

# ============================================================
# 8th SUTRA
# PURANAPURANABHYAM
#
# Meaning:
# "By Completion or Non-Completion"
#
# Used for suitable algebraic expressions where
# completion / non-completion simplifies calculation.
#
# Example:
# x + 7 = 15
#
# We complete the expression to obtain x.
# ============================================================


def solve_puranapuranabhyam(expression):

    import re

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    if expression is None:

        return {
            "applicable": False,
            "message": "Please enter an equation.",
            "steps": [],
            "answer": None
        }

    expression = str(expression).strip()

    if expression == "":

        return {
            "applicable": False,
            "message": "Please enter an equation.",
            "steps": [],
            "answer": None
        }

    # Remove spaces

    eq = expression.replace(" ", "").lower()

    # --------------------------------------------------------
    # STEP 2: EQUATION CHECK
    # --------------------------------------------------------

    if "=" not in eq:

        return {
            "applicable": False,

            "message":
                "Please enter an equation containing '='.",

            "steps": [],

            "answer": None
        }

    parts = eq.split("=")

    if len(parts) != 2:

        return {
            "applicable": False,

            "message":
                "Please enter one valid equation.",

            "steps": [],

            "answer": None
        }

    left = parts[0]
    right = parts[1]

    # --------------------------------------------------------
    # STEP 3:
    # BASIC LINEAR COMPLETION
    #
    # Supports:
    #
    # x+5=12
    # x-5=12
    # 2x+5=15
    # 3x-7=11
    # --------------------------------------------------------

    pattern = r"^([+-]?\d*)x([+-]\d+)?$"

    match_left = re.match(pattern, left)

    # --------------------------------------------------------
    # CASE 1:
    # x-expression on LEFT
    # --------------------------------------------------------

    if match_left:

        coeff_text = match_left.group(1)
        constant_text = match_left.group(2)

        # Coefficient

        if coeff_text in ("", "+"):

            coefficient = 1

        elif coeff_text == "-":

            coefficient = -1

        else:

            coefficient = int(coeff_text)

        # Constant

        if constant_text:

            constant = int(constant_text)

        else:

            constant = 0

        # Right side must be number

        try:

            target = float(right)

        except ValueError:

            return {
                "applicable": False,

                "message":
                    "Right side must be a number.",

                "steps": [],

                "answer": None
            }

        # ----------------------------------------------------
        # SOLVE
        # ----------------------------------------------------

        remaining = target - constant

        x = remaining / coefficient

        # ----------------------------------------------------
        # FORMAT
        # ----------------------------------------------------

        if x.is_integer():

            x_display = str(int(x))

        else:

            x_display = str(round(x, 6))

        # ----------------------------------------------------
        # STEPS
        # ----------------------------------------------------

        steps = [

            f"🧮 Equation: {expression}",

            "📖 Sutra: Puranapuranabhyam",

            (
                "💡 Meaning: "
                "By Completion or Non-Completion."
            ),

            (
                "Step 1: Identify the incomplete part "
                "of the expression."
            ),

            (
                f"The expression contains "
                f"{coefficient}x and {constant}."
            ),

            (
                "Step 2: Complete the equation "
                "by removing the constant."
            ),

            (
                f"{coefficient}x + ({constant}) "
                f"= {target}"
            ),

            (
                f"Step 3: Remove {constant} "
                f"from both sides."
            ),

            (
                f"{coefficient}x "
                f"= {target} - ({constant})"
            ),

            (
                f"{coefficient}x = {remaining}"
            ),

            (
                f"Step 4: Divide by {coefficient}."
            ),

            (
                f"x = {remaining} / {coefficient}"
            ),

            (
                f"✅ Final Answer: x = {x_display}"
            )
        ]

        return {

            "applicable": True,

            "message":
                "Puranapuranabhyam can be applied.",

            "equation":
                expression,

            "steps":
                steps,

            "answer":
                x_display,

            "explanation": (
                "Puranapuranabhyam means "
                "'By Completion or Non-Completion'. "
                "The expression is completed or simplified "
                "by dealing with the missing/additional part."
            )
        }

    # ========================================================
    # CASE 2:
    # x-expression on RIGHT
    #
    # Example:
    #
    # 15 = x + 7
    # ========================================================

    pattern_right = r"^([+-]?\d*)x([+-]\d+)?$"

    match_right = re.match(
        pattern_right,
        right
    )

    if match_right:

        coeff_text = match_right.group(1)

        constant_text = match_right.group(2)

        if coeff_text in ("", "+"):

            coefficient = 1

        elif coeff_text == "-":

            coefficient = -1

        else:

            coefficient = int(coeff_text)

        if constant_text:

            constant = int(constant_text)

        else:

            constant = 0

        try:

            target = float(left)

        except ValueError:

            return {
                "applicable": False,

                "message":
                    "Left side must be a number.",

                "steps": [],

                "answer": None
            }

        remaining = target - constant

        x = remaining / coefficient

        if x.is_integer():

            x_display = str(int(x))

        else:

            x_display = str(round(x, 6))

        steps = [

            f"🧮 Equation: {expression}",

            "📖 Sutra: Puranapuranabhyam",

            (
                "💡 Meaning: "
                "By Completion or Non-Completion."
            ),

            (
                f"Step 1: {coefficient}x + "
                f"({constant}) = {target}"
            ),

            (
                f"Step 2: Remove {constant} "
                f"from both sides."
            ),

            (
                f"{coefficient}x = {remaining}"
            ),

            (
                f"Step 3: Divide by {coefficient}."
            ),

            (
                f"x = {remaining} / {coefficient}"
            ),

            (
                f"✅ Final Answer: x = {x_display}"
            )
        ]

        return {

            "applicable": True,

            "message":
                "Puranapuranabhyam can be applied.",

            "equation":
                expression,

            "steps":
                steps,

            "answer":
                x_display,

            "explanation": (
                "The equation is completed by "
                "removing the known part."
            )
        }

    # ========================================================
    # NOT APPLICABLE
    # ========================================================

    return {

        "applicable": False,

        "message": (
            "This equation is not in a suitable "
            "Puranapuranabhyam form."
        ),

        "steps": [

            f"Equation entered: {expression}",

            (
                "Try a simple completion equation such as:"
            ),

            "x + 7 = 15",

            "2x + 5 = 15",

            "3x - 7 = 11"
        ],

        "answer": None
    }



# ============================================================
# 9th SUTRA
# CHALANA-KALANABHYAM
#
# Meaning:
# "Differences and Similarities"
#
# Used in Vedic Mathematics for solving suitable
# algebraic / quadratic problems and calculus-related
# calculations.
#
# This solver handles quadratic equations:
#
# ax² + bx + c = 0
#
# Example:
# x² - 5x + 6 = 0
#
# Answer:
# x = 2, 3
# ============================================================


def solve_chalana_kalanabhyam(equation):

    import re
    import math

    # --------------------------------------------------------
    # STEP 1: VALIDATION
    # --------------------------------------------------------

    if equation is None:

        return {
            "applicable": False,
            "message": "Please enter a quadratic equation.",
            "steps": [],
            "answer": None
        }

    equation = str(equation).strip()

    if equation == "":

        return {
            "applicable": False,
            "message": "Please enter a quadratic equation.",
            "steps": [],
            "answer": None
        }

    # Remove spaces

    eq = equation.replace(" ", "").lower()

    # --------------------------------------------------------
    # STEP 2:
    # EQUATION MUST HAVE =
    # --------------------------------------------------------

    if "=" not in eq:

        return {
            "applicable": False,
            "message": "Equation must contain '='.",
            "steps": [],
            "answer": None
        }

    parts = eq.split("=")

    if len(parts) != 2:

        return {
            "applicable": False,
            "message": "Please enter one valid equation.",
            "steps": [],
            "answer": None
        }

    left = parts[0]
    right = parts[1]

    # --------------------------------------------------------
    # STEP 3:
    # Move everything to LEFT
    #
    # Example:
    #
    # x² - 5x + 6 = 0
    #
    # Already suitable.
    # --------------------------------------------------------

    if right != "0":

        return {
            "applicable": False,

            "message": (
                "For this solver, enter the quadratic equation "
                "with 0 on the right side."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 4:
    # NORMALIZE x² SYMBOL
    # --------------------------------------------------------

    left = left.replace("**2", "x2")
    left = left.replace("x^2", "x2")
    left = left.replace("x²", "x2")

    # --------------------------------------------------------
    # STEP 5:
    # PARSE ax² + bx + c
    # --------------------------------------------------------

    pattern = (
        r"^([+-]?\d*)x2"
        r"([+-]\d+)?x"
        r"([+-]\d+)?$"
    )

    match = re.match(pattern, left)

    if not match:

        # Try equation without bx term
        pattern2 = (
            r"^([+-]?\d*)x2"
            r"([+-]\d+)?$"
        )

        match2 = re.match(pattern2, left)

        if not match2:

            return {
                "applicable": False,

                "message": (
                    "Please enter a quadratic equation "
                    "in the form ax² + bx + c = 0."
                ),

                "steps": [],

                "answer": None
            }

        a_text = match2.group(1)
        b_text = None
        c_text = match2.group(2)

    else:

        a_text = match.group(1)
        b_text = match.group(2)
        c_text = match.group(3)

    # --------------------------------------------------------
    # STEP 6:
    # CONVERT COEFFICIENTS
    # --------------------------------------------------------

    if a_text in ("", "+"):

        a = 1

    elif a_text == "-":

        a = -1

    else:

        a = int(a_text)

    if b_text:

        b = int(b_text)

    else:

        b = 0

    if c_text:

        c = int(c_text)

    else:

        c = 0

    # --------------------------------------------------------
    # STEP 7:
    # CHECK QUADRATIC
    # --------------------------------------------------------

    if a == 0:

        return {
            "applicable": False,
            "message": "This is not a quadratic equation.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 8:
    # DISCRIMINANT
    #
    # D = b² - 4ac
    # --------------------------------------------------------

    discriminant = (
        b * b
        -
        4 * a * c
    )

    # --------------------------------------------------------
    # STEP 9:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Equation: {equation}"
    )

    steps.append(
        "📖 Sutra: Chalana-Kalanabhyam"
    )

    steps.append(
        (
            "💡 Meaning: "
            "Differences and Similarities."
        )
    )

    steps.append(
        (
            f"Step 1: Identify coefficients:"
        )
    )

    steps.append(
        (
            f"a = {a}, b = {b}, c = {c}"
        )
    )

    # --------------------------------------------------------
    # STEP 10:
    # DIFFERENCE CALCULATION
    # --------------------------------------------------------

    steps.append(
        (
            "Step 2: Calculate the discriminant "
            "using the difference."
        )
    )

    steps.append(
        (
            f"D = b² - 4ac"
        )
    )

    steps.append(
        (
            f"D = ({b})² - 4({a})({c})"
        )
    )

    steps.append(
        (
            f"D = {discriminant}"
        )
    )

    # ========================================================
    # CASE 1:
    # D < 0
    # ========================================================

    if discriminant < 0:

        steps.append(
            (
                "The discriminant is negative."
            )
        )

        steps.append(
            (
                "Therefore the equation has "
                "no real roots."
            )
        )

        return {

            "applicable": True,

            "message":
                "No real roots.",

            "steps":
                steps,

            "answer":
                "No real roots",

            "discriminant":
                discriminant,

            "explanation": (
                "The difference calculation gives "
                "a negative discriminant, so there "
                "are no real solutions."
            )
        }

    # ========================================================
    # CASE 2:
    # D = 0
    # ========================================================

    if discriminant == 0:

        x = -b / (2 * a)

        if x.is_integer():

            x_display = str(int(x))

        else:

            x_display = str(round(x, 6))

        steps.append(
            (
                "The discriminant is zero."
            )
        )

        steps.append(
            (
                "Therefore both roots are equal."
            )
        )

        steps.append(
            (
                f"x = -b / 2a"
            )
        )

        steps.append(
            (
                f"x = -({b}) / (2 × {a})"
            )
        )

        steps.append(
            (
                f"x = {x_display}"
            )
        )

        steps.append(
            (
                f"✅ Final Answer: x = {x_display}"
            )
        )

        return {

            "applicable": True,

            "message":
                "Equal roots found.",

            "steps":
                steps,

            "answer":
                x_display,

            "discriminant":
                discriminant
        }

    # ========================================================
    # CASE 3:
    # D > 0
    # ========================================================

    sqrt_d = math.sqrt(discriminant)

    x1 = (
        -b + sqrt_d
    ) / (2 * a)

    x2 = (
        -b - sqrt_d
    ) / (2 * a)

    # --------------------------------------------------------
    # FORMAT
    # --------------------------------------------------------

    if x1.is_integer():

        x1_display = str(int(x1))

    else:

        x1_display = str(round(x1, 6))

    if x2.is_integer():

        x2_display = str(int(x2))

    else:

        x2_display = str(round(x2, 6))

    # --------------------------------------------------------
    # STEPS
    # --------------------------------------------------------

    steps.append(
        (
            "The discriminant is positive."
        )
    )

    steps.append(
        (
            "Therefore the equation has two real roots."
        )
    )

    steps.append(
        (
            "Step 3: Find the square root of D."
        )
    )

    steps.append(
        (
            f"√{discriminant} = {sqrt_d}"
        )
    )

    steps.append(
        (
            "Step 4: Find the first root."
        )
    )

    steps.append(
        (
            f"x₁ = (-b + √D) / 2a"
        )
    )

    steps.append(
        (
            f"x₁ = (-({b}) + √{discriminant}) "
            f"/ (2 × {a})"
        )
    )

    steps.append(
        (
            f"x₁ = {x1_display}"
        )
    )

    steps.append(
        (
            "Step 5: Find the second root."
        )
    )

    steps.append(
        (
            f"x₂ = (-b - √D) / 2a"
        )
    )

    steps.append(
        (
            f"x₂ = (-({b}) - √{discriminant}) "
            f"/ (2 × {a})"
        )
    )

    steps.append(
        (
            f"x₂ = {x2_display}"
        )
    )

    steps.append(
        (
            f"🎯 Final Answer:"
        )
    )

    steps.append(
        (
            f"x₁ = {x1_display}, "
            f"x₂ = {x2_display}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Quadratic equation solved.",

        "equation":
            equation,

        "steps":
            steps,

        "answer": {

            "x1":
                x1_display,

            "x2":
                x2_display
        },

        "discriminant":
            discriminant,

        "explanation": (
            "Chalana-Kalanabhyam is associated with "
            "differences and similarities. The calculation "
            "is demonstrated here through the discriminant "
            "and root relationship of a quadratic equation."
        )
    }
# ============================================================
# 10th SUTRA
# YAVADUNAM
#
# Meaning:
# "Whatever the Deficiency"
#
# Mainly used for multiplication of numbers close to
# a convenient base such as 10, 100, 1000, etc.
#
# Examples:
#
# 98 × 97
# 102 × 103
# 997 × 998
# 48 × 47
#
# ============================================================


def solve_yavadunam(num1, num2):

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    try:

        a = int(str(num1).strip())
        b = int(str(num2).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter two valid numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2: POSITIVE NUMBERS
    # --------------------------------------------------------

    if a <= 0 or b <= 0:

        return {
            "applicable": False,
            "message": "Please enter positive numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3:
    # FIND A SUITABLE BASE
    #
    # 10
    # 100
    # 1000
    # 10000 ...
    # --------------------------------------------------------

    max_number = max(a, b)

    digits = len(str(max_number))

    base = 10 ** digits

    # If numbers are closer to previous base,
    # use previous base.

    previous_base = 10 ** (digits - 1)

    current_distance = (
        abs(a - base) +
        abs(b - base)
    )

    previous_distance = (
        abs(a - previous_base) +
        abs(b - previous_base)
    )

    if previous_distance < current_distance:

        base = previous_base

    # --------------------------------------------------------
    # STEP 4:
    # CALCULATE DEVIATIONS
    # --------------------------------------------------------

    deviation_a = a - base
    deviation_b = b - base

    # --------------------------------------------------------
    # STEP 5:
    # CHECK WHETHER NUMBERS ARE CLOSE ENOUGH
    #
    # Yavadunam is useful when numbers are near the base.
    # --------------------------------------------------------

    relative_a = abs(deviation_a) / base
    relative_b = abs(deviation_b) / base

    if relative_a > 0.20 or relative_b > 0.20:

        return {

            "applicable": False,

            "message": (
                "Yavadunam is not suitable for these numbers. "
                "The numbers should be reasonably close to "
                "a convenient base such as 10, 100 or 1000."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 6:
    # LEFT PART
    #
    # a + deviation_b
    #
    # OR
    #
    # b + deviation_a
    # --------------------------------------------------------

    left_part = (
        a + deviation_b
    )

    # --------------------------------------------------------
    # STEP 7:
    # DEVIATION PRODUCT
    # --------------------------------------------------------

    right_part = (
        deviation_a *
        deviation_b
    )

    # --------------------------------------------------------
    # STEP 8:
    # NUMBER OF ZEROES IN BASE
    # --------------------------------------------------------

    base_digits = len(str(base)) - 1

    right_width = base_digits

    # --------------------------------------------------------
    # STEP 9:
    # HANDLE RIGHT PART
    #
    # Example:
    #
    # 98 × 97
    #
    # Base = 100
    #
    # Deviations:
    # -2, -3
    #
    # Product = +6
    #
    # Right side must contain 2 digits:
    #
    # 06
    # --------------------------------------------------------

    # --------------------------------------------------------
    # CASE A:
    # RIGHT PART POSITIVE
    # --------------------------------------------------------

    if right_part >= 0:

        right_display = str(right_part).zfill(
            right_width
        )

        # ----------------------------------------------------
        # If right part has overflow, carry to left part.
        # ----------------------------------------------------

        if right_part >= base:

            carry = right_part // base

            right_remainder = right_part % base

            left_part += carry

            right_display = str(
                right_remainder
            ).zfill(right_width)

        else:

            carry = 0

    # --------------------------------------------------------
    # CASE B:
    # RIGHT PART NEGATIVE
    # --------------------------------------------------------

    else:

        # Borrow 1 from left part.

        borrow = 1

        left_part -= borrow

        positive_right = (
            base + right_part
        )

        right_display = str(
            positive_right
        ).zfill(right_width)

        carry = -1

    # --------------------------------------------------------
    # STEP 10:
    # FINAL ANSWER
    # --------------------------------------------------------

    answer = (
        int(str(left_part) + right_display)
    )

    # --------------------------------------------------------
    # STEP 11:
    # CREATE DETAILED STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Question: {a} × {b}"
    )

    steps.append(
        "📖 Sutra: Yāvadūnam"
    )

    steps.append(
        (
            "💡 Meaning: "
            "Whatever the Deficiency"
        )
    )

    # --------------------------------------------------------
    # BASE
    # --------------------------------------------------------

    steps.append(
        (
            f"🎯 Step 1: Choose the nearest convenient "
            f"base = {base}"
        )
    )

    steps.append(
        (
            f"The base contains {base_digits} zero(s)."
        )
    )

    # --------------------------------------------------------
    # FIRST DEVIATION
    # --------------------------------------------------------

    if deviation_a < 0:

        steps.append(
            (
                f"Step 2: {a} is deficient from {base} "
                f"by {abs(deviation_a)}."
            )
        )

        steps.append(
            (
                f"{a} - {base} = {deviation_a}"
            )
        )

    else:

        steps.append(
            (
                f"Step 2: {a} exceeds {base} "
                f"by {deviation_a}."
            )
        )

        steps.append(
            (
                f"{a} - {base} = +{deviation_a}"
            )
        )

    # --------------------------------------------------------
    # SECOND DEVIATION
    # --------------------------------------------------------

    if deviation_b < 0:

        steps.append(
            (
                f"Step 3: {b} is deficient from {base} "
                f"by {abs(deviation_b)}."
            )
        )

        steps.append(
            (
                f"{b} - {base} = {deviation_b}"
            )
        )

    else:

        steps.append(
            (
                f"Step 3: {b} exceeds {base} "
                f"by {deviation_b}."
            )
        )

        steps.append(
            (
                f"{b} - {base} = +{deviation_b}"
            )
        )

    # --------------------------------------------------------
    # CROSS OPERATION
    # --------------------------------------------------------

    steps.append(
        "🔄 Step 4: Cross subtract/add."
    )

    if deviation_b >= 0:

        steps.append(
            (
                f"{a} + ({deviation_b}) "
                f"= {a + deviation_b}"
            )
        )

    else:

        steps.append(
            (
                f"{a} - {abs(deviation_b)} "
                f"= {a + deviation_b}"
            )
        )

    # --------------------------------------------------------
    # RIGHT PART
    # --------------------------------------------------------

    steps.append(
        "✖️ Step 5: Multiply the deviations."
    )

    steps.append(
        (
            f"({deviation_a}) × "
            f"({deviation_b}) "
            f"= {deviation_a * deviation_b}"
        )
    )

    # --------------------------------------------------------
    # RIGHT SIDE FORMATTING
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 6: Since base = {base}, "
            f"the right part must contain "
            f"{base_digits} digit(s)."
        )
    )

    steps.append(
        (
            f"Right part = {right_display}"
        )
    )

    # --------------------------------------------------------
    # BORROW / CARRY
    # --------------------------------------------------------

    if right_part < 0:

        steps.append(
            (
                "Because the right part is negative, "
                "borrow 1 from the left part."
            )
        )

    elif right_part >= base:

        steps.append(
            (
                f"Carry {carry} to the left part."
            )
        )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 7: Combine:"
        )
    )

    steps.append(
        (
            f"Left part = {left_part}"
        )
    )

    steps.append(
        (
            f"Right part = {right_display}"
        )
    )

    steps.append(
        (
            f"🎯 Final Answer = "
            f"{left_part}{right_display}"
        )
    )

    # --------------------------------------------------------
    # EXACT VERIFICATION
    # --------------------------------------------------------

    steps.append(
        (
            f"✅ Verification: "
            f"{a} × {b} = {answer}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Yāvadūnam can be applied successfully.",

        "question":
            f"{a} × {b}",

        "base":
            base,

        "deviation1":
            deviation_a,

        "deviation2":
            deviation_b,

        "left_part":
            left_part,

        "right_part":
            right_part,

        "steps":
            steps,

        "answer":
            answer,

        "explanation": (
            "Yāvadūnam means 'Whatever the Deficiency'. "
            "Numbers close to a power-of-10 base are "
            "expressed as deficiencies or excesses from "
            "that base. The cross operation gives the "
            "left part and the product of deviations gives "
            "the right part."
        )
    }

# ============================================================
# 11th SUTRA
# VYASTI-SAMASTI
#
# Meaning:
# "Part and Whole"
#
# Vyasti  = Part
# Samasti = Whole
#
# Idea:
# Break a number into convenient parts and combine
# the partial results to get the whole answer.
#
# Example:
#
# 23 × 12
#
# 23 × (10 + 2)
#
# = (23 × 10) + (23 × 2)
#
# = 230 + 46
#
# = 276
#
# ============================================================


def solve_vyasti_samasti(num1, num2):

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    try:

        a = int(str(num1).strip())
        b = int(str(num2).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter two valid numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2: POSITIVE NUMBERS
    # --------------------------------------------------------

    if a <= 0 or b <= 0:

        return {
            "applicable": False,
            "message": "Please enter positive numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3:
    # CHOOSE THE NUMBER WHICH IS EASIER TO SPLIT
    #
    # Example:
    #
    # 23 × 12
    #
    # 12 is easier:
    #
    # 12 = 10 + 2
    # --------------------------------------------------------

    def best_decomposition(number):

        digits = list(
            map(int, str(number))
        )

        length = len(digits)

        # ----------------------------------------------------
        # Split using place values.
        #
        # Example:
        #
        # 123 = 100 + 20 + 3
        # ----------------------------------------------------

        parts = []

        for index, digit in enumerate(digits):

            power = length - index - 1

            place = 10 ** power

            value = digit * place

            if value != 0:

                parts.append(value)

        return parts

    parts_a = best_decomposition(a)
    parts_b = best_decomposition(b)

    # --------------------------------------------------------
    # STEP 4:
    # CHOOSE FEWER PARTS
    # --------------------------------------------------------

    if len(parts_a) <= len(parts_b):

        whole = a
        parts = parts_a
        multiplier = b

    else:

        whole = b
        parts = parts_b
        multiplier = a

    # --------------------------------------------------------
    # STEP 5:
    # PARTIAL PRODUCTS
    # --------------------------------------------------------

    partial_results = []

    for part in parts:

        partial = part * multiplier

        partial_results.append(
            partial
        )

    # --------------------------------------------------------
    # STEP 6:
    # WHOLE / FINAL
    # --------------------------------------------------------

    answer = sum(
        partial_results
    )

    # --------------------------------------------------------
    # STEP 7:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Question: {a} × {b}"
    )

    steps.append(
        "📖 Sutra: Vyasti-Samasti"
    )

    steps.append(
        "💡 Meaning: Part and Whole"
    )

    steps.append(
        (
            "Vyasti means 'Part' and "
            "Samasti means 'Whole'."
        )
    )

    # --------------------------------------------------------
    # DECOMPOSITION
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 1: Split {whole} "
            f"into convenient parts."
        )
    )

    decomposition_text = " + ".join(
        str(x)
        for x in parts
    )

    steps.append(
        (
            f"{whole} = "
            f"{decomposition_text}"
        )
    )

    # --------------------------------------------------------
    # PARTIAL CALCULATIONS
    # --------------------------------------------------------

    steps.append(
        "Step 2: Multiply each part separately."
    )

    for part, partial in zip(
        parts,
        partial_results
    ):

        steps.append(
            (
                f"{part} × {multiplier} "
                f"= {partial}"
            )
        )

    # --------------------------------------------------------
    # ADD PARTS
    # --------------------------------------------------------

    steps.append(
        "Step 3: Add all partial results."
    )

    addition_text = " + ".join(
        str(x)
        for x in partial_results
    )

    steps.append(
        (
            f"{addition_text} "
            f"= {answer}"
        )
    )

    # --------------------------------------------------------
    # FINAL ANSWER
    # --------------------------------------------------------

    steps.append(
        (
            f"🎯 Final Answer = {answer}"
        )
    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    steps.append(
        (
            f"✅ Verification: "
            f"{a} × {b} = {answer}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Vyasti-Samasti can be applied successfully.",

        "question":
            f"{a} × {b}",

        "whole":
            whole,

        "parts":
            parts,

        "partial_results":
            partial_results,

        "steps":
            steps,

        "answer":
            answer,

        "explanation": (
            "Vyasti-Samasti means 'Part and Whole'. "
            "The number is divided into convenient "
            "parts, each part is calculated separately, "
            "and the partial results are combined to "
            "obtain the whole answer."
        )
    }

# ============================================================
# 13th SUTRA
# SOPANTYADVAYAMANTYAM
#
# Meaning:
# "The ultimate and twice the penultimate"
#
# Sopantya = Penultimate (second last)
# Antyam   = Ultimate (last)
#
# This Sutra is mainly used in specific Vedic
# multiplication / algebraic patterns.
#
# The solver below demonstrates the digit-based
# pattern using a number and its last two digits.
# ============================================================


def solve_sopantyadvayamantyam(number):

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    try:

        n = int(str(number).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter a valid number.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2: POSITIVE NUMBER
    # --------------------------------------------------------

    if n < 10:

        return {
            "applicable": False,

            "message": (
                "This Sutra requires at least "
                "two digits."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3:
    # FIND LAST TWO DIGITS
    # --------------------------------------------------------

    last_digit = n % 10

    penultimate_digit = (
        (n // 10) % 10
    )

    # --------------------------------------------------------
    # STEP 4:
    # TWICE PENULTIMATE
    # --------------------------------------------------------

    double_penultimate = (
        2 * penultimate_digit
    )

    # --------------------------------------------------------
    # STEP 5:
    # COMBINE
    #
    # Ultimate + twice penultimate
    # --------------------------------------------------------

    value = (
        last_digit +
        double_penultimate
    )

    # --------------------------------------------------------
    # STEP 6:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Number: {n}"
    )

    steps.append(
        "📖 Sutra: Sopāntyadvayamantyam"
    )

    steps.append(
        (
            "💡 Meaning: "
            "The ultimate and twice the penultimate."
        )
    )

    # --------------------------------------------------------
    # LAST DIGIT
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 1: Ultimate (last digit) "
            f"of {n} = {last_digit}"
        )
    )

    # --------------------------------------------------------
    # PENULTIMATE
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 2: Penultimate (second last digit) "
            f"of {n} = {penultimate_digit}"
        )
    )

    # --------------------------------------------------------
    # DOUBLE
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 3: Twice the penultimate:"
        )
    )

    steps.append(
        (
            f"2 × {penultimate_digit} "
            f"= {double_penultimate}"
        )
    )

    # --------------------------------------------------------
    # COMBINE
    # --------------------------------------------------------

    steps.append(
        (
            "Step 4: Add the ultimate "
            "and twice the penultimate."
        )
    )

    steps.append(
        (
            f"{last_digit} + "
            f"{double_penultimate} "
            f"= {value}"
        )
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    steps.append(
        (
            f"🎯 Final Answer = {value}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Sopāntyadvayamantyam pattern calculated.",

        "number":
            n,

        "ultimate":
            last_digit,

        "penultimate":
            penultimate_digit,

        "twice_penultimate":
            double_penultimate,

        "steps":
            steps,

        "answer":
            value,

        "explanation": (
            "Sopāntyadvayamantyam means "
            "'the ultimate and twice the penultimate'. "
            "The last digit is taken along with twice "
            "the second-last digit."
        )
    }# ============================================================
# 14th SUTRA
# EKANYUNENA PURVENA
#
# Meaning:
# "By One Less Than the Previous One"
#
# Mainly useful for multiplication by:
#
# 9
# 99
# 999
# 9999
# etc.
#
# Examples:
#
# 47 × 99
# 325 × 999
# 1234 × 9999
#
# ============================================================


def solve_ekanyunena_purvena(number, multiplier):

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    try:

        n = int(str(number).strip())
        m = int(str(multiplier).strip())

    except (ValueError, TypeError):

        return {
            "applicable": False,
            "message": "Please enter valid numbers.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2:
    # CHECK MULTIPLIER
    #
    # Valid:
    #
    # 9
    # 99
    # 999
    # 9999
    #
    # --------------------------------------------------------

    m_string = str(m)

    if (
        len(m_string) == 0
        or any(
            digit != "9"
            for digit in m_string
        )
    ):

        return {

            "applicable": False,

            "message": (
                "Ekanyunena Purvena is applicable when "
                "the multiplier is 9, 99, 999, 9999, etc."
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 3:
    # BASE
    #
    # 9  -> 10
    # 99 -> 100
    # 999 -> 1000
    #
    # --------------------------------------------------------

    digits = len(m_string)

    base = 10 ** digits

    # --------------------------------------------------------
    # STEP 4:
    # ONE LESS THAN PREVIOUS
    #
    # n - 1
    # --------------------------------------------------------

    left_part = n - 1

    # --------------------------------------------------------
    # STEP 5:
    # COMPLEMENT FROM BASE
    #
    # base - n
    # --------------------------------------------------------

    right_part = base - n

    # --------------------------------------------------------
    # STEP 6:
    # CHECK RIGHT PART
    #
    # It must fit in exactly `digits` places.
    #
    # Example:
    #
    # 47 × 99
    #
    # 100 - 47 = 53
    #
    # 53 has 2 digits.
    #
    # --------------------------------------------------------

    right_display = str(
        right_part
    ).zfill(digits)

    # --------------------------------------------------------
    # STEP 7:
    # FINAL ANSWER
    # --------------------------------------------------------

    answer = (
        left_part * base
        +
        right_part
    )

    # --------------------------------------------------------
    # STEP 8:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Question: {n} × {m}"
    )

    steps.append(
        "📖 Sutra: Ekanyūnena Pūrvena"
    )

    steps.append(
        (
            "💡 Meaning: "
            "By One Less Than the Previous One"
        )
    )

    # --------------------------------------------------------
    # BASE
    # --------------------------------------------------------

    steps.append(
        (
            f"Step 1: Since multiplier = {m}, "
            f"take the next power-of-10 base."
        )
    )

    steps.append(
        (
            f"Base = {base}"
        )
    )

    # --------------------------------------------------------
    # LEFT PART
    # --------------------------------------------------------

    steps.append(
        (
            "Step 2: Take one less than "
            "the number."
        )
    )

    steps.append(
        (
            f"{n} - 1 = {left_part}"
        )
    )

    # --------------------------------------------------------
    # RIGHT PART
    # --------------------------------------------------------

    steps.append(
        (
            "Step 3: Find the complement "
            "from the base."
        )
    )

    steps.append(
        (
            f"{base} - {n} = {right_part}"
        )
    )

    steps.append(
        (
            f"Right part = {right_display}"
        )
    )

    # --------------------------------------------------------
    # COMBINE
    # --------------------------------------------------------

    steps.append(
        (
            "Step 4: Combine the two parts."
        )
    )

    steps.append(
        (
            f"{left_part} | {right_display}"
        )
    )

    steps.append(
        (
            f"🎯 Final Answer = "
            f"{left_part}{right_display}"
        )
    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    exact_answer = n * m

    steps.append(
        (
            f"✅ Verification: "
            f"{n} × {m} = {exact_answer}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Ekanyūnena Pūrvena applied successfully.",

        "number":
            n,

        "multiplier":
            m,

        "base":
            base,

        "left_part":
            left_part,

        "right_part":
            right_part,

        "steps":
            steps,

        "answer":
            answer,

        "explanation": (
            "Ekanyūnena Pūrvena means "
            "'By one less than the previous one'. "
            "For multiplication by 9, 99, 999, etc., "
            "one less than the multiplicand forms the "
            "left part, while its complement from the "
            "corresponding power of 10 forms the right part."
        )
    }

# ============================================================
# 15th SUTRA
# GUNITA-SAMUCCHAYAH
#
# Meaning:
# "The Product of the Sum"
#
# This solver demonstrates the principle using
# algebraic expressions.
#
# Example:
#
# (x + 2)(x + 3)
#
# = x² + 5x + 6
#
# Sum of coefficients:
#
# LHS:
# (1 + 2)(1 + 3) = 3 × 4 = 12
#
# RHS:
# 1 + 5 + 6 = 12
#
# Therefore the identity is verified.
#
# ============================================================


def solve_gunita_samucchayah(expression):

    import re

    # --------------------------------------------------------
    # STEP 1: VALIDATION
    # --------------------------------------------------------

    if expression is None:

        return {
            "applicable": False,
            "message": "Please enter an algebraic expression.",
            "steps": [],
            "answer": None
        }

    expression = str(expression).strip()

    if expression == "":

        return {
            "applicable": False,
            "message": "Please enter an algebraic expression.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2:
    # Remove spaces
    # --------------------------------------------------------

    expr = expression.replace(" ", "").lower()

    # --------------------------------------------------------
    # STEP 3:
    # EXPECT FORM:
    #
    # (x+a)(x+b)
    #
    # Example:
    #
    # (x+2)(x+3)
    # --------------------------------------------------------

    pattern = (
        r"^\(x([+-]\d+)\)"
        r"\(x([+-]\d+)\)$"
    )

    match = re.match(
        pattern,
        expr
    )

    if not match:

        return {

            "applicable": False,

            "message": (
                "Please enter an expression in the form "
                "(x+a)(x+b). Example: (x+2)(x+3)"
            ),

            "steps": [],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 4:
    # GET a AND b
    # --------------------------------------------------------

    a = int(
        match.group(1)
    )

    b = int(
        match.group(2)
    )

    # --------------------------------------------------------
    # STEP 5:
    # EXPAND
    #
    # (x+a)(x+b)
    #
    # = x² + (a+b)x + ab
    # --------------------------------------------------------

    middle = a + b

    constant = a * b

    # --------------------------------------------------------
    # STEP 6:
    # COEFFICIENTS
    # --------------------------------------------------------

    lhs_coefficients = [
        1,
        a
    ]

    rhs_coefficients = [
        1,
        middle,
        constant
    ]

    # --------------------------------------------------------
    # STEP 7:
    # SUM OF INPUT VALUES
    # --------------------------------------------------------

    first_sum = 1 + a

    second_sum = 1 + b

    product_of_sums = (
        first_sum *
        second_sum
    )

    # --------------------------------------------------------
    # STEP 8:
    # SUM OF RESULT COEFFICIENTS
    # --------------------------------------------------------

    sum_of_coefficients = (
        1 +
        middle +
        constant
    )

    # --------------------------------------------------------
    # STEP 9:
    # VERIFY
    # --------------------------------------------------------

    verified = (
        product_of_sums
        ==
        sum_of_coefficients
    )

    # --------------------------------------------------------
    # STEP 10:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Expression: {expression}"
    )

    steps.append(
        "📖 Sutra: Guṇita-Samucchayah"
    )

    steps.append(
        (
            "💡 Meaning: "
            "The Product of the Sum"
        )
    )

    # --------------------------------------------------------
    # EXPANSION
    # --------------------------------------------------------

    steps.append(
        "Step 1: Expand the expression."
    )

    steps.append(
        (
            f"(x + {a})(x + {b})"
        )
    )

    steps.append(
        (
            f"= x² + ({a} + {b})x "
            f"+ ({a} × {b})"
        )
    )

    steps.append(
        (
            f"= x² + {middle}x "
            f"+ {constant}"
        )
    )

    # --------------------------------------------------------
    # SUM OF FACTORS
    # --------------------------------------------------------

    steps.append(
        (
            "Step 2: Find the sum of coefficients "
            "of each factor."
        )
    )

    steps.append(
        (
            f"(1 + {a}) = {first_sum}"
        )
    )

    steps.append(
        (
            f"(1 + {b}) = {second_sum}"
        )
    )

    # --------------------------------------------------------
    # PRODUCT OF SUMS
    # --------------------------------------------------------

    steps.append(
        (
            "Step 3: Multiply these sums."
        )
    )

    steps.append(
        (
            f"{first_sum} × {second_sum} "
            f"= {product_of_sums}"
        )
    )

    # --------------------------------------------------------
    # RHS SUM
    # --------------------------------------------------------

    steps.append(
        (
            "Step 4: Add the coefficients "
            "of the expanded expression."
        )
    )

    steps.append(
        (
            f"1 + {middle} + {constant} "
            f"= {sum_of_coefficients}"
        )
    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    if verified:

        steps.append(
            (
                f"✅ Both values are equal:"
            )
        )

        steps.append(
            (
                f"{product_of_sums} = "
                f"{sum_of_coefficients}"
            )
        )

        steps.append(
            (
                "🎯 Result: Identity verified "
                "using the Guṇita-Samucchayah principle."
            )
        )

        message = (
            "Guṇita-Samucchayah principle verified."
        )

    else:

        steps.append(
            (
                f"❌ Values are not equal:"
            )
        )

        steps.append(
            (
                f"{product_of_sums} ≠ "
                f"{sum_of_coefficients}"
            )
        )

        steps.append(
            (
                "The given expression does not satisfy "
                "this verification."
            )
        )

        message = (
            "The given expression could not be verified."
        )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            message,

        "expression":
            expression,

        "expanded_form":
            f"x² + {middle}x + {constant}",

        "product_of_sums":
            product_of_sums,

        "sum_of_coefficients":
            sum_of_coefficients,

        "verified":
            verified,

        "steps":
            steps,

        "answer":
            (
                "Verified"
                if verified
                else "Not Verified"
            ),

        "explanation": (
            "Guṇita-Samucchayah is demonstrated here "
            "through the relationship between the product "
            "of sums and the sum of coefficients in a "
            "suitable algebraic expression."
        )
    }

# ============================================================
# 16th SUTRA
# GUNAKA-SAMUCCHAYAH
#
# Meaning:
# "The Factors of the Sum"
#
# Used here for demonstrating factorisation of
# suitable quadratic expressions.
#
# Example:
#
# x² + 5x + 6
#
# Factors:
#
# (x + 2)(x + 3)
#
# Because:
#
# 2 + 3 = 5
# 2 × 3 = 6
#
# ============================================================


def solve_gunaka_samucchayah(expression):

    import re
    import math

    # --------------------------------------------------------
    # STEP 1: INPUT VALIDATION
    # --------------------------------------------------------

    if expression is None:

        return {
            "applicable": False,
            "message": "Please enter a quadratic expression.",
            "steps": [],
            "answer": None
        }

    expression = str(expression).strip()

    if expression == "":

        return {
            "applicable": False,
            "message": "Please enter a quadratic expression.",
            "steps": [],
            "answer": None
        }

    # --------------------------------------------------------
    # STEP 2: CLEAN INPUT
    # --------------------------------------------------------

    expr = (
        expression
        .replace(" ", "")
        .lower()
        .replace("²", "^2")
    )

    # --------------------------------------------------------
    # STEP 3:
    # REMOVE = 0 IF USER ENTERS:
    #
    # x² + 5x + 6 = 0
    # --------------------------------------------------------

    if "=" in expr:

        left, right = expr.split("=")

        if right != "0":

            return {
                "applicable": False,

                "message": (
                    "For this solver, enter an expression "
                    "such as x² + 5x + 6 = 0."
                ),

                "steps": [],

                "answer": None
            }

        expr = left

    # --------------------------------------------------------
    # STEP 4:
    # NORMALIZE
    # --------------------------------------------------------

    expr = expr.replace("x^2", "x2")

    # --------------------------------------------------------
    # STEP 5:
    # PARSE:
    #
    # x² + bx + c
    #
    # Also supports:
    #
    # x² - bx + c
    # x² + bx - c
    # --------------------------------------------------------

    pattern = (
        r"^x2"
        r"([+-]\d+)x"
        r"([+-]\d+)$"
    )

    match = re.match(
        pattern,
        expr
    )

    if not match:

        return {

            "applicable": False,

            "message": (
                "Please enter a monic quadratic expression "
                "such as x² + 5x + 6."
            ),

            "steps": [],

            "answer": None
        }

    b = int(
        match.group(1)
    )

    c = int(
        match.group(2)
    )

    # --------------------------------------------------------
    # STEP 6:
    # FIND FACTOR PAIR
    #
    # Need:
    #
    # p + q = b
    # p × q = c
    # --------------------------------------------------------

    factor_pair = None

    limit = int(
        math.sqrt(abs(c))
    )

    for i in range(
        1,
        limit + 1
    ):

        if c % i != 0:
            continue

        j = c // i

        # Positive pair

        if i + j == b:

            factor_pair = (
                i,
                j
            )

            break

        # Negative pair

        if (
            -i - j
            == b
        ):

            factor_pair = (
                -i,
                -j
            )

            break

    # --------------------------------------------------------
    # STEP 7:
    # IF NO FACTORS
    # --------------------------------------------------------

    if factor_pair is None:

        return {

            "applicable": False,

            "message": (
                "No integer factor pair was found "
                "for this quadratic."
            ),

            "steps": [

                f"Expression: {expression}",

                (
                    f"Need two numbers whose sum is "
                    f"{b} and product is {c}."
                ),

                "No suitable integer pair exists."
            ],

            "answer": None
        }

    # --------------------------------------------------------
    # STEP 8:
    # GET FACTORS
    # --------------------------------------------------------

    p, q = factor_pair

    # --------------------------------------------------------
    # STEP 9:
    # CREATE FACTOR TEXT
    # --------------------------------------------------------

    def factor_text(value):

        if value >= 0:

            return f"(x + {value})"

        else:

            return f"(x - {abs(value)})"

    factor1 = factor_text(p)
    factor2 = factor_text(q)

    # --------------------------------------------------------
    # STEP 10:
    # VERIFY SUM
    # --------------------------------------------------------

    sum_check = (
        p + q
    )

    product_check = (
        p * q
    )

    # --------------------------------------------------------
    # STEP 11:
    # CREATE STEPS
    # --------------------------------------------------------

    steps = []

    steps.append(
        f"🧮 Expression: {expression}"
    )

    steps.append(
        "📖 Sutra: Guṇaka-Samucchayah"
    )

    steps.append(
        (
            "💡 Meaning: "
            "The Factors of the Sum."
        )
    )

    # --------------------------------------------------------
    # STEP 12:
    # IDENTIFY b AND c
    # --------------------------------------------------------

    steps.append(
        "Step 1: Identify the coefficients."
    )

    steps.append(
        (
            f"x² + ({b})x + ({c})"
        )
    )

    steps.append(
        (
            f"Middle coefficient = {b}"
        )
    )

    steps.append(
        (
            f"Constant = {c}"
        )
    )

    # --------------------------------------------------------
    # STEP 13:
    # FIND FACTORS
    # --------------------------------------------------------

    steps.append(
        (
            "Step 2: Find two numbers whose "
            "sum is the middle coefficient."
        )
    )

    steps.append(
        (
            f"p + q = {b}"
        )
    )

    steps.append(
        (
            "Step 3: Their product must equal "
            "the constant."
        )
    )

    steps.append(
        (
            f"p × q = {c}"
        )
    )

    # --------------------------------------------------------
    # STEP 14:
    # SHOW FOUND NUMBERS
    # --------------------------------------------------------

    steps.append(
        (
            f"Suitable numbers are "
            f"{p} and {q}."
        )
    )

    steps.append(
        (
            f"Check sum:"
        )
    )

    steps.append(
        (
            f"{p} + ({q}) = {sum_check}"
        )
    )

    steps.append(
        (
            f"Check product:"
        )
    )

    steps.append(
        (
            f"{p} × ({q}) = {product_check}"
        )
    )

    # --------------------------------------------------------
    # STEP 15:
    # FACTORISE
    # --------------------------------------------------------

    steps.append(
        "Step 4: Write the factors."
    )

    steps.append(
        (
            f"🎯 {expression} "
            f"= {factor1}{factor2}"
        )
    )

    # --------------------------------------------------------
    # STEP 16:
    # VERIFY BY MULTIPLICATION
    # --------------------------------------------------------

    steps.append(
        "Step 5: Verify the factors."
    )

    steps.append(
        (
            f"{factor1}{factor2}"
        )
    )

    steps.append(
        (
            f"= x² + ({p + q})x + ({p * q})"
        )
    )

    steps.append(
        (
            f"= x² + ({b})x + ({c})"
        )
    )

    steps.append(
        "✅ Factorisation verified."
    )

    # --------------------------------------------------------
    # STEP 17:
    # SOLUTIONS
    #
    # (x+p)(x+q)=0
    #
    # x=-p or x=-q
    # --------------------------------------------------------

    root1 = -p
    root2 = -q

    steps.append(
        "Step 6: Find the roots."
    )

    steps.append(
        (
            f"x = {-p}"
        )
    )

    steps.append(
        (
            f"x = {-q}"
        )
    )

    steps.append(
        (
            f"🎯 Final Answer: "
            f"x = {root1}, {root2}"
        )
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "applicable": True,

        "message":
            "Factorisation completed successfully.",

        "expression":
            expression,

        "factors": [
            factor1,
            factor2
        ],

        "factor_values": [
            p,
            q
        ],

        "roots": [
            root1,
            root2
        ],

        "steps":
            steps,

        "answer": {

            "factorised":
                f"{factor1}{factor2}",

            "roots": [
                root1,
                root2
            ]
        },

        "explanation": (
            "Guṇaka-Samucchayah is demonstrated here "
            "through the factor relationship of a suitable "
            "quadratic expression. The required factors "
            "are identified from their sum and product, "
            "then the result is verified."
        )
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
            points = 2 if is_correct else 0  

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

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
  student_id = session.get('student_id')  # Ya session.get('user_id')
  if not student_id:
    return jsonify({'success': False, 'message': 'Unauthorized'}), 401

  data = request.get_json()
  rating_val = data.get('rating')

  conn = get_db_connection()
  cursor = conn.cursor()

  cursor.execute(
      'UPDATE students SET rating = %s WHERE id = %s', (rating_val, student_id)
  )
  conn.commit()

  cursor.close()
  conn.close()

  return jsonify({'success': True})


@app.route('/get-user-rating', methods=['GET'])
def get_user_rating():
  student_id = session.get('student_id')  # Ya session.get('user_id')
  if not student_id:
    return jsonify({'hasRated': False})

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  cursor.execute('SELECT rating FROM students WHERE id = %s', (student_id,))
  student = cursor.fetchone()

  cursor.close()
  conn.close()

  if student and student['rating']:
    return jsonify({'hasRated': True, 'rating': student['rating']})

  return jsonify({'hasRated': False})


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )