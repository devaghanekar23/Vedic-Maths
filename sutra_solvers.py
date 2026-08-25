# ============================================================
# sutra_solvers.py
# Solve-functions + practice/streak helpers used by app.py
#
# app.py expects:
#   - solve_sutra(sutra_id, num1, num2) -> dict with keys:
#       "success", "result", "steps", "message", "hint"
#   - update_streak(cursor, student_id)
#   - get_practice_stats(cursor, student_id) -> dict with keys:
#       "total_attempts", "correct_attempts",
#       "sutras_attempted", "sutras_mastered"
# ============================================================

from datetime import date, timedelta

# --------------------------------------------------------
# Mastery thresholds used by get_practice_stats()
# --------------------------------------------------------
MIN_ATTEMPTS_FOR_MASTERY = 5
MASTERY_THRESHOLD = 0.7  # 70% correct


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
    if num2 == 0:
        return {"success": False, "message": "Division by zero is not allowed."}

    q, r = divmod(num1, num2)

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
    ans = num1 - num2

    steps = [
        f"Equation: x + {num2} = {num1}",
        f"Step 1 (Apply Sutra): Express as sum equated to zero -> x + ({num2} - {num1}) = 0",
        f"Step 2 (Simplify Constant): x + ({num2 - num1}) = 0",
        f"Step 3 (Solve for x): Transpose constant term -> x = {ans}",
        f"Final Answer = x = {ans}"
    ]

    return {"success": True, "result": f"x = {ans}", "steps": steps}


def solve_sutra_6(num1, num2):
    primary_base = 100
    working_base = 50
    k = working_base / primary_base

    dev1 = num1 - working_base
    dev2 = num2 - working_base

    cross_sum = num1 + dev2
    adjusted_left = cross_sum * k
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
    sum_val = num1
    diff_val = num2

    x = (sum_val + diff_val) / 2
    y = (sum_val - diff_val) / 2

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

    return {"success": True, "result": f"x = {x_str}, y = {y_str}", "steps": steps}


def solve_sutra_8(num1, num2):
    ans = num1 + num2

    rem1 = num1 % 10
    rem2 = num2 % 10

    if (10 - rem1) <= (10 - rem2) and rem1 != 0:
        target, helper = num1, num2
    else:
        target, helper = num2, num1

    deficiency = (10 - (target % 10)) % 10

    if deficiency == 0:
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
    num_str = str(abs(num1))
    digits = len(num_str)
    base = 10 ** digits if num1 > (10 ** digits) / 2 else 10 ** (digits - 1)
    if base < 10:
        base = 10

    base_zeros = len(str(base)) - 1
    dev = num1 - base

    left_part = num1 + dev
    right_part = dev ** 2
    ans = num1 * num1

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
    ans = num1 * num2

    tens_part = (num2 // 10) * 10
    units_part = num2 % 10

    if tens_part == 0 or units_part == 0:
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
    if num2 == 0:
        return {"success": False, "message": "Division by zero is not allowed."}

    q = num1 // num2
    prod = q * num2
    r = num1 - prod

    steps = [
        f"Question: Find Remainder of {num1} ÷ {num2}",
        f"Step 1 (Find Quotient): {num1} ÷ {num2} gives Quotient (Q) = {q}",
        f"Step 2 (Multiply Quotient by Divisor): {q} × {num2} = {prod}",
        f"Step 3 (Calculate Remainder): Dividend - (Quotient × Divisor) -> {num1} - {prod} = {r}",
        f"Final Answer = Remainder {r}"
    ]

    return {"success": True, "result": f"R = {r}", "steps": steps}


def solve_sutra_13(num1, num2):
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
    multiplier_str = str(num2)
    if not set(multiplier_str).issubset({'9'}):
        ans = num1 * num2
        return {
            "success": True,
            "result": str(ans),
            "steps": [f"Direct Multiplication: {num1} × {num2} = {ans}"]
        }

    left = num1 - 1
    right = num2 - left
    ans = num1 * num2

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
    b = num1 + num2
    c = num1 * num2

    if b > 0:
        b_str = f" + {b}x"
    elif b < 0:
        b_str = f" - {abs(b)}x"
    else:
        b_str = ""

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


# ============================================================
# DISPATCHER - used by app.py's routes
# ============================================================

def solve_sutra(sutra_id, num1, num2=0):
    solvers = {
        1: solve_sutra_1, 2: solve_sutra_2, 3: solve_sutra_3, 4: solve_sutra_4,
        5: solve_sutra_5, 6: solve_sutra_6, 7: solve_sutra_7, 8: solve_sutra_8,
        9: solve_sutra_9, 10: solve_sutra_10, 11: solve_sutra_11, 12: solve_sutra_12,
        13: solve_sutra_13, 14: solve_sutra_14, 15: solve_sutra_15, 16: solve_sutra_16
    }
    try:
        sutra_id = int(sutra_id)
    except (ValueError, TypeError):
        return {"success": False, "message": "Invalid Sutra ID."}

    solver = solvers.get(sutra_id)
    return solver(num1, num2) if solver else {"success": False, "message": "Solver not found."}


# ============================================================
# STREAK + PRACTICE-STATS HELPERS - used by app.py's routes
# ============================================================

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
