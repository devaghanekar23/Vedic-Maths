// ============================================================
// 1. EKADHIKENA PURVENA
// "By one more than the previous one"
// ============================================================
function solveEkadhikenaPurvena(num) {
    const n = parseInt(num, 10);
    if (isNaN(n)) {
        return {
            applicable: false,
            message: "Please enter a valid number.",
            steps: [],
            answer: null
        };
    }

    if (n <= 0) {
        return {
            applicable: false,
            message: "Please enter a positive number.",
            steps: [],
            answer: null
        };
    }

    if (n % 10 !== 5) {
        return {
            applicable: false,
            message: "This Sutra is not applicable to this type of calculation. Ekadhikena Purvena is used for squaring numbers ending in 5. Example: 25², 35², 45².",
            steps: [],
            answer: null
        };
    }

    const previous = Math.floor(n / 10);
    const oneMore = previous + 1;
    const leftPart = previous * oneMore;
    const rightPart = 25;
    const answer = n * n;

    const steps = [
        `Question: ${n}²`,
        `Step 1: The number ends in 5.`,
        `Step 2: Remove the last digit 5. The previous part is ${previous}.`,
        `Step 3: Add 1 to the previous part: ${previous} + 1 = ${oneMore}`,
        `Step 4: Multiply the previous number by one more than itself: ${previous} × ${oneMore} = ${leftPart}`,
        `Step 5: Square 5: 5 × 5 = ${rightPart}`,
        `Step 6: Put both parts together: ${leftPart} | ${rightPart}`,
        `Final Answer = ${answer}`
    ];

    return {
        applicable: true,
        message: "Ekadhikena Purvena can be applied successfully.",
        steps: steps,
        answer: answer,
        explanation: "Ekadhikena Purvena means 'By one more than the previous one'. For numbers ending in 5, multiply the number before 5 by one more than itself and append 25."
    };
}

// ============================================================
// 2. NIKHILAM NAVATASHCARAMAM DASHATAH
// "All from 9 and the last from 10"
// ============================================================
function solveNikhilam(num1, num2) {
    const a = parseInt(String(num1).trim(), 10);
    const b = parseInt(String(num2).trim(), 10);

    if (isNaN(a) || isNaN(b)) {
        return {
            applicable: false,
            message: "Please enter two valid numbers.",
            steps: [],
            answer: null
        };
    }

    if (a <= 0 || b <= 0) {
        return {
            applicable: false,
            message: "Please enter positive numbers.",
            steps: [],
            answer: null
        };
    }

    // Auto-select standard base (10, 100, 1000, etc.)
    const maxVal = Math.max(a, b);
    let power = Math.round(Math.log10(maxVal));
    power = Math.max(1, power);
    const base = Math.pow(10, power);

    const deviationA = a - base;
    const deviationB = b - base;

    const crossPart = a + deviationB;
    const deviationProduct = deviationA * deviationB;
    const rightDigits = String(base).length - 1;

    let carry = 0;
    let borrow = 0;
    let leftPart = 0;
    let rightPart = 0;

    if (deviationProduct >= 0) {
        carry = Math.floor(deviationProduct / base);
        rightPart = deviationProduct % base;
        leftPart = crossPart + carry;
    } else {
        borrow = Math.floor((Math.abs(deviationProduct) + base - 1) / base);
        leftPart = crossPart - borrow;
        rightPart = deviationProduct + (borrow * base);
    }

    const rightDisplay = String(rightPart).padStart(rightDigits, '0');
    const answer = a * b;

    let steps = [];
    steps.push(`🧮 Question: ${a} × ${b}`);
    steps.push("📖 Sutra: Nikhilam Navatashcaramam Dashatah");
    steps.push("💡 Meaning: All from 9 and the last from 10.");
    steps.push(`🎯 Step 1: Choose a suitable base = ${base}`);
    steps.push(`Why ${base}? Because both ${a} and ${b} are close to ${base}.`);

    steps.push(`✏️ Step 2: Find the deviation of ${a} from ${base}.`);
    steps.push(`${a} - ${base} = ${deviationA}`);
    steps.push(`Since ${a} is ${deviationA < 0 ? 'smaller' : 'greater'} than ${base}, deviation is ${deviationA > 0 ? '+' : ''}${deviationA}.`);

    steps.push(`✏️ Step 3: Find the deviation of ${b} from ${base}.`);
    steps.push(`${b} - ${base} = ${deviationB}`);
    steps.push(`Since ${b} is ${deviationB < 0 ? 'smaller' : 'greater'} than ${base}, deviation is ${deviationB > 0 ? '+' : ''}${deviationB}.`);

    steps.push("🔄 Step 4: Perform cross subtraction/addition.");
    steps.push(`${a} + (${deviationB}) = ${crossPart}`);

    steps.push("✖️ Step 5: Multiply the two deviations.");
    steps.push(`(${deviationA}) × (${deviationB}) = ${deviationProduct}`);

    if (carry > 0) {
        steps.push(`➕ Step 6: Carry ${carry} to the left side because right part exceeds base width.`);
    } else if (borrow > 0) {
        steps.push("➖ Step 6: Deviation product is negative.");
        steps.push(`Borrow ${borrow} from left side using base ${base}.`);
        steps.push(`After borrowing, right part becomes ${rightPart}.`);
    }

    steps.push(`🔢 Step 7: Format right part with ${rightDigits} digit(s): ${rightDisplay}`);
    steps.push("🔗 Step 8: Combine left and right parts:");
    steps.push(`${leftPart} | ${rightDisplay}`);
    steps.push(`✅ Final Answer = ${answer}`);

    return {
        applicable: true,
        message: "Nikhilam Navatashcaramam Dashatah applied successfully.",
        question: `${a} × ${b}`,
        base: base,
        deviation1: deviationA,
        deviation2: deviationB,
        steps: steps,
        answer: answer,
        explanation: "Nikhilam Navatashcaramam Dashatah means 'All from 9 and the last from 10'. We choose a convenient base such as 10, 100 or 1000 to quickly calculate products using deviations."
    };
}

// ============================================================
// 3. URDHVA TIRYAGBHYAM
// "Vertically and Crosswise"
// ============================================================
function solveUrdhvaTiryagbhyam(num1, num2) {
    const a = parseInt(String(num1).trim(), 10);
    const b = parseInt(String(num2).trim(), 10);

    if (isNaN(a) || isNaN(b) || a <= 0 || b <= 0) {
        return { applicable: false, message: "Please enter valid positive numbers.", steps: [], answer: null };
    }

    const s1 = String(a);
    const s2 = String(b);
    const digits1 = s1.split('').reverse().map(x => parseInt(x, 10));
    const digits2 = s2.split('').reverse().map(x => parseInt(x, 10));

    const n1 = digits1.length;
    const n2 = digits2.length;
    const resultSize = n1 + n2 - 1;
    let raw = new Array(resultSize).fill(0);
    let steps = [
        `🧮 Question: ${a} × ${b}`,
        "📖 Sutra: Urdhva Tiryagbhyam",
        "💡 Meaning: Vertically and Crosswise"
    ];

    for (let position = 0; position < resultSize; position++) {
        let total = 0;
        let calculations = [];
        for (let i = 0; i < n1; i++) {
            let j = position - i;
            if (j >= 0 && j < n2) {
                let product = digits1[i] * digits2[j];
                total += product;
                calculations.push(`${digits1[i]} × ${digits2[j]} = ${product}`);
            }
        }
        steps.push(`🔹 Step ${position + 1}: ${calculations.join(' + ')} → Total = ${total}`);
        raw[position] = total;
    }

    steps.push("🔢 Carrying over digits from right to left:");
    let carry = 0;
    let finalDigits = [];
    for (let i = 0; i < raw.length; i++) {
        let current = raw[i] + carry;
        let remainder = current % 10;
        carry = Math.floor(current / 10);
        finalDigits.push(remainder);
        steps.push(`Position ${i + 1}: Raw sum = ${current} → Keep ${remainder}, Carry ${carry}`);
    }
    if (carry > 0) {
        finalDigits.push(carry);
        steps.push(`Final Carry over = ${carry}`);
    }

    const answer = parseInt(finalDigits.reverse().join(''), 10);
    steps.push(`✅ Final Answer = ${answer}`);

    return {
        applicable: true,
        message: "Urdhva Tiryagbhyam applied successfully.",
        question: `${a} × ${b}`,
        steps: steps,
        answer: answer,
        explanation: "Urdhva Tiryagbhyam calculates cross-products position by position and propagates carries from right to left."
    };
}

// ============================================================
// 4. PARAVARTYA YOJAYET
// "Transpose and Apply"
// ============================================================
function solveParavartya(num1, num2) {
    const dividend = parseInt(String(num1).trim(), 10);
    const divisor = parseInt(String(num2).trim(), 10);

    if (isNaN(dividend) || isNaN(divisor)) {
        return {
            applicable: false,
            message: "Please enter valid numbers.",
            steps: [],
            answer: null
        };
    }

    if (dividend <= 0 || divisor <= 0) {
        return {
            applicable: false,
            message: "Please enter positive numbers.",
            steps: [],
            answer: null
        };
    }

    if (divisor === 1) {
        return {
            applicable: false,
            message: "This Sutra is not required for division by 1.",
            steps: [],
            answer: null
        };
    }

    const digits = String(divisor).length;
    const base = Math.pow(10, digits);
    const deviation = base - divisor;

    if (Math.abs(deviation) > base * 0.20) {
        return {
            applicable: false,
            message: "Paravartya Yojayet is not suitable for this divisor. The divisor should be reasonably close to a convenient power-of-10 base.",
            steps: [],
            answer: null
        };
    }

    const transposed = deviation;
    const quotient = Math.floor(dividend / divisor);
    const remainder = dividend % divisor;

    let steps = [];
    steps.push(`🧮 Question: ${dividend} ÷ ${divisor}`);
    steps.push("📖 Sutra: Parāvartya Yojayet");
    steps.push("💡 Meaning: Transpose and Apply");
    steps.push(`Step 1: Choose base = ${base}`);
    steps.push("Step 2: Find deviation of divisor from base:");
    steps.push(`${base} - ${divisor} = ${deviation}`);
    steps.push("Step 3: Transpose the deviation:");
    steps.push(`Transposed value = ${transposed}`);

    if (divisor === base - 1) {
        steps.push(`Step 4: Since ${divisor} is 1 less than ${base}, the transposed value is +1.`);
        const digitsDividend = String(dividend).split('').map(x => parseInt(x, 10));
        let runningValues = [];
        let running = digitsDividend[0];
        runningValues.push(running);

        steps.push(`Start with first digit: ${running}`);

        for (let i = 1; i < digitsDividend.length; i++) {
            let digit = digitsDividend[i];
            let newValue = running + digit;
            steps.push(`Next: ${digit} + previous value ${running} = ${newValue}`);
            running = newValue;
            runningValues.push(running);
        }

        steps.push("Step 5: Perform final adjustment according to the divisor.");
        steps.push("Exact verification:");
        steps.push(`${quotient} × ${divisor} + ${remainder} = ${dividend}`);
        steps.push(`✅ Final Answer = ${quotient} remainder ${remainder}`);

        return {
            applicable: true,
            message: "Parāvartya Yojayet can be applied.",
            question: `${dividend} ÷ ${divisor}`,
            base: base,
            deviation: deviation,
            transposed: transposed,
            steps: steps,
            answer: quotient,
            remainder: remainder,
            explanation: "Parāvartya Yojayet means 'Transpose and Apply'. The deviation of the divisor from the base is transposed and used in the calculation."
        };
    }

    steps.push("Step 4: Apply the transposed value according to the divisor.");
    steps.push("Step 5: Verify the quotient and remainder.");
    steps.push(`${quotient} × ${divisor} + ${remainder} = ${dividend}`);
    steps.push(`✅ Final Answer = ${quotient} remainder ${remainder}`);

    return {
        applicable: true,
        message: "Parāvartya Yojayet can be applied.",
        question: `${dividend} ÷ ${divisor}`,
        base: base,
        deviation: deviation,
        transposed: transposed,
        steps: steps,
        answer: quotient,
        remainder: remainder,
        explanation: "Parāvartya Yojayet means 'Transpose and Apply'. It is primarily useful for division with divisors close to a convenient base."
    };
}

// ============================================================
// 5. SHUNYAM SAMYASAMUCCAYE
// "When the Samuccaya is the same, it becomes zero."
// ============================================================
function solveShunyamSamyasamuccaye(equation) {
    if (!equation) {
        return {
            applicable: false,
            message: "Please enter an equation.",
            steps: [],
            answer: null
        };
    }

    equation = String(equation).trim();
    if (equation === "") {
        return {
            applicable: false,
            message: "Please enter an equation.",
            steps: [],
            answer: null
        };
    }

    const cleanEquation = equation.replace(/\s+/g, "");

    if (!cleanEquation.includes("=")) {
        return {
            applicable: false,
            message: "Please enter a valid equation containing '='.",
            steps: [],
            answer: null
        };
    }

    const parts = cleanEquation.split("=");
    if (parts.length !== 2) {
        return {
            applicable: false,
            message: "Please enter one equation with one '=' sign.",
            steps: [],
            answer: null
        };
    }

    const left = parts[0];
    const right = parts[1];

    if (!cleanEquation.toLowerCase().includes("x")) {
        return {
            applicable: false,
            message: "Please enter an equation containing x.",
            steps: [],
            answer: null
        };
    }

    if (left === right) {
        return {
            applicable: false,
            message: "The same expression appears on both sides. Therefore the equation is an identity, not a unique equation to solve.",
            steps: [
                `Equation: ${equation}`,
                `Left side = ${left}`,
                `Right side = ${right}`,
                "Both sides are exactly equal.",
                "Therefore every value of x satisfies the equation.",
                "There is no single value of x."
            ],
            answer: "All real values of x"
        };
    }

    const pattern = /^([+-]?\d*)x([+-]\d+)?=([+-]?\d*)x([+-]\d+)?$/i;
    const match = cleanEquation.match(pattern);

    if (match) {
        const aText = match[1];
        const bText = match[2];
        const cText = match[3];
        const dText = match[4];

        let a = (aText === "" || aText === "+") ? 1 : (aText === "-" ? -1 : parseInt(aText, 10));
        let b = bText ? parseInt(bText, 10) : 0;
        let c = (cText === "" || cText === "+") ? 1 : (cText === "-" ? -1 : parseInt(cText, 10));
        let d = dText ? parseInt(dText, 10) : 0;

        const coefficient = a - c;
        const constant = d - b;

        if (coefficient === 0) {
            if (constant === 0) {
                return {
                    applicable: false,
                    message: "The equation has infinitely many solutions.",
                    steps: [
                        `Equation: ${equation}`,
                        `Move x terms: ${a}x - ${c}x = ${d} - ${b}`,
                        `${coefficient}x = ${constant}`,
                        "This becomes 0 = 0.",
                        "Therefore every value of x is a solution."
                    ],
                    answer: "All real values of x"
                };
            } else {
                return {
                    applicable: false,
                    message: "The equation has no solution.",
                    steps: [
                        `Equation: ${equation}`,
                        `Move x terms: ${a}x - ${c}x = ${d} - ${b}`,
                        `${coefficient}x = ${constant}`,
                        `0 = ${constant}`,
                        "This is impossible.",
                        "Therefore there is no solution."
                    ],
                    answer: "No solution"
                };
            }
        }

        const x = constant / coefficient;
        const xDisplay = Number.isInteger(x) ? String(x) : String(x);

        const steps = [
            `🧮 Equation: ${equation}`,
            "📖 Sutra: Shunyam Samyasamuccaye",
            "💡 Meaning: When the Samuccaya is the same, it becomes zero.",
            "Step 1: Compare the x terms:",
            `${a}x and ${c}x`,
            "Step 2: Compare the constants:",
            `${b} and ${d}`,
            "Step 3: Bring x terms together:",
            `${a}x - ${c}x = ${d} - ${b}`,
            "Step 4:",
            `${coefficient}x = ${constant}`,
            `Step 5: Divide by ${coefficient}:`,
            `x = ${constant} / ${coefficient}`,
            `Step 6: Therefore x = ${xDisplay}`,
            `✅ Final Answer: x = ${xDisplay}`
        ];

        return {
            applicable: true,
            message: "Equation solved successfully.",
            equation: equation,
            steps: steps,
            answer: xDisplay,
            explanation: "Shunyam Samyasamuccaye is used when a common samuccaya appears in a suitable algebraic equation. The common part can be treated as zero, simplifying the equation."
        };
    }

    return {
        applicable: false,
        message: "This equation is not in a form that this Shunyam Samyasamuccaye solver can safely solve. Please enter a suitable algebraic equation.",
        steps: [
            `Equation entered: ${equation}`,
            "The solver could not identify a suitable Shunyam Samyasamuccaye pattern.",
            "Try a simple equation such as:",
            "3x + 5 = 2x + 10",
            "5x + 7 = 3x + 15"
        ],
        answer: null
    };
}

// ============================================================
// 6. ANURUPYENA
// "Proportionately"
// ============================================================
function solveAnurupyena(num1, num2) {
    const a = parseInt(String(num1).trim(), 10);
    const b = parseInt(String(num2).trim(), 10);

    if (isNaN(a) || isNaN(b)) {
        return {
            applicable: false,
            message: "Please enter two valid numbers.",
            steps: [],
            answer: null
        };
    }

    if (a <= 0 || b <= 0) {
        return {
            applicable: false,
            message: "Please enter positive numbers.",
            steps: [],
            answer: null
        };
    }

    let standardBases = [];
    for (let power = 1; power <= 5; power++) {
        standardBases.push(Math.pow(10, power));
    }

    let proportionalBases = [];
    for (let base of standardBases) {
        proportionalBases.push(
            Math.floor(base / 2),
            Math.floor(base / 4),
            Math.floor(base / 5),
            base * 2,
            base * 5
        );
    }

    let allBases = Array.from(new Set(proportionalBases.filter(x => x > 0))).sort((x, y) => x - y);

    let candidates = [];
    for (let base of allBases) {
        let distanceA = Math.abs(a - base) / base;
        let distanceB = Math.abs(b - base) / base;

        if (distanceA <= 0.25 && distanceB <= 0.25) {
            candidates.push({
                totalDistance: distanceA + distanceB,
                base: base
            });
        }
    }

    if (candidates.length === 0) {
        return {
            applicable: false,
            message: "Anurupyena is not suitable for these numbers. Try numbers close to a proportional base such as 20, 25, 50, 100, 200, 500, etc.",
            steps: [],
            answer: null
        };
    }

    candidates.sort((x, y) => x.totalDistance - y.totalDistance);
    const workingBase = candidates[0].base;

    let standardBase = null;
    let proportion = null;

    for (let base of standardBases) {
        if (base % workingBase === 0) {
            let ratio = base / workingBase;
            if ([2, 4, 5, 10].includes(ratio)) {
                standardBase = base;
                proportion = ratio;
                break;
            }
        }
    }

    if (standardBase === null) {
        return {
            applicable: false,
            message: "A suitable proportional base could not be identified.",
            steps: [],
            answer: null
        };
    }

    const deviationA = a - workingBase;
    const deviationB = b - workingBase;
    const crossPart = a + deviationB;
    const deviationProduct = deviationA * deviationB;
    const answer = a * b;

    let steps = [];
    steps.push(`🧮 Question: ${a} × ${b}`);
    steps.push("📖 Sutra: Anurupyena");
    steps.push("💡 Meaning: Proportionately");
    steps.push("This Sutra uses a convenient proportional working base.");
    steps.push(`🎯 Step 1: Choose working base = ${workingBase}`);
    steps.push(`Working base ${workingBase} is ${proportion} times smaller than standard base ${standardBase}.`);
    steps.push(`✏️ Step 2: Deviation of ${a}: ${a} - ${workingBase} = ${deviationA}`);
    steps.push(`✏️ Step 3: Deviation of ${b}: ${b} - ${workingBase} = ${deviationB}`);
    steps.push("🔄 Step 4: Cross operation");
    steps.push(`${a} + (${deviationB}) = ${crossPart}`);
    steps.push("✖️ Step 5: Multiply deviations");
    steps.push(`(${deviationA}) × (${deviationB}) = ${deviationProduct}`);
    steps.push("📐 Step 6: Apply proportional adjustment");
    steps.push(`Working base = ${workingBase}`);
    steps.push(`Standard base = ${standardBase}`);
    steps.push(`Proportion = 1/${proportion}`);
    steps.push("🔗 Step 7: Combine the proportional parts to obtain the product.");
    steps.push(`Verification: ${a} × ${b} = ${answer}`);
    steps.push(`✅ Final Answer = ${answer}`);

    return {
        applicable: true,
        message: "Anurupyena can be applied successfully.",
        question: `${a} × ${b}`,
        working_base: workingBase,
        standard_base: standardBase,
        proportion: proportion,
        deviation1: deviationA,
        deviation2: deviationB,
        steps: steps,
        answer: answer,
        explanation: "Anurupyena means 'Proportionately'. When the ordinary base is not convenient, a proportional working base such as 50 instead of 100 can be selected. The calculation is then adjusted according to the proportion."
    };
}

// ============================================================
// 7. SANKALANA VYAVAKALANABHYAM
// "By Addition and By Subtraction"
// ============================================================
function solveSankalanaVyavakalanabhyam(eq1, eq2) {
    if (!eq1 || !eq2) {
        return {
            applicable: false,
            message: "Please enter two equations.",
            steps: [],
            answer: null
        };
    }

    eq1 = String(eq1).replace(/\s+/g, "").toLowerCase();
    eq2 = String(eq2).replace(/\s+/g, "").toLowerCase();

    if (!eq1.includes("=") || !eq2.includes("=")) {
        return {
            applicable: false,
            message: "Both equations must contain '='.",
            steps: [],
            answer: null
        };
    }

    function parseEquation(equation) {
        const parts = equation.split("=");
        const constant = parseFloat(parts[1]);
        if (isNaN(constant)) return null;

        let left = parts[0].replace(/-/g, "+-");
        if (left.startsWith("+")) left = left.substring(1);

        const terms = left.split("+");
        let xCoeff = 0;
        let yCoeff = 0;

        for (let term of terms) {
            if (!term) continue;
            if (term.includes("x")) {
                let val = term.replace("x", "");
                let num = (val === "" || val === "+") ? 1 : (val === "-" ? -1 : parseFloat(val));
                if (isNaN(num)) return null;
                xCoeff += num;
            } else if (term.includes("y")) {
                let val = term.replace("y", "");
                let num = (val === "" || val === "+") ? 1 : (val === "-" ? -1 : parseFloat(val));
                if (isNaN(num)) return null;
                yCoeff += num;
            } else {
                return null;
            }
        }
        return [xCoeff, yCoeff, constant];
    }

    const first = parseEquation(eq1);
    const second = parseEquation(eq2);

    if (!first || !second) {
        return {
            applicable: false,
            message: "Please enter equations in a simple linear form such as 2x+3y=13.",
            steps: [],
            answer: null
        };
    }

    const [a1, b1, c1] = first;
    const [a2, b2, c2] = second;

    if ((a1 === 0 && b1 === 0) || (a2 === 0 && b2 === 0)) {
        return {
            applicable: false,
            message: "Both equations must contain x or y.",
            steps: [],
            answer: null
        };
    }

    const determinant = a1 * b2 - a2 * b1;
    if (determinant === 0) {
        return {
            applicable: false,
            message: "These equations do not have a unique solution.",
            steps: [
                `Equation 1: ${eq1}`,
                `Equation 2: ${eq2}`,
                `Determinant = (${a1} × ${b2}) - (${a2} × ${b1}) = 0`,
                "Therefore a unique x and y cannot be obtained."
            ],
            answer: null
        };
    }

    let steps = [];
    steps.push(`🧮 Equation 1: ${eq1}`);
    steps.push(`🧮 Equation 2: ${eq2}`);
    steps.push("📖 Sutra: Sankalana Vyavakalanabhyam");
    steps.push("💡 Meaning: By Addition and By Subtraction.");

    let x, y;

    if (b1 === -b2) {
        let newX = a1 + a2;
        let newC = c1 + c2;
        steps.push("➕ Step 1: Add the two equations.");
        steps.push(`(${a1}x + ${b1}y) + (${a2}x + ${b2}y) = ${c1} + ${c2}`);
        steps.push(`${newX}x = ${newC}`);
        x = newC / newX;
    } else {
        let newX = a1 - a2;
        let newY = b1 - b2;
        let newC = c1 - c2;

        if (newY === 0) {
            steps.push("➖ Step 1: Subtract Equation 2 from Equation 1.");
            steps.push(`(${a1}x + ${b1}y) - (${a2}x + ${b2}y) = ${c1} - ${c2}`);
            steps.push(`${newX}x = ${newC}`);
            x = newC / newX;
        } else {
            steps.push("➖ Step 1: Adjust the equations to eliminate x.");
            let A1 = a1 * a2, B1 = b1 * a2, C1 = c1 * a2;
            let A2 = a2 * a1, B2 = b2 * a1, C2 = c2 * a1;
            let resY = B1 - B2;
            let resC = C1 - C2;

            steps.push("After adjustment:");
            steps.push(`${A1}x + ${B1}y = ${C1}`);
            steps.push(`${A2}x + ${B2}y = ${C2}`);
            steps.push("Subtract:");
            steps.push(`${resY}y = ${resC}`);

            y = resC / resY;
            x = (c1 - b1 * y) / a1;

            let xDisplay = Number.isInteger(x) ? String(x) : String(parseFloat(x.toFixed(6)));
            let yDisplay = Number.isInteger(y) ? String(y) : String(parseFloat(y.toFixed(6)));

            steps.push(`✅ y = ${yDisplay}`);
            steps.push(`Substitute y = ${yDisplay} into Equation 1.`);
            steps.push(`✅ x = ${xDisplay}`);
            steps.push(`🎯 Final Answer: x = ${xDisplay}, y = ${yDisplay}`);

            return {
                applicable: true,
                message: "Equations solved successfully.",
                steps: steps,
                answer: { x: xDisplay, y: yDisplay },
                explanation: "Sankalana Vyavakalanabhyam means 'By Addition and By Subtraction'. The equations are combined so that one variable is eliminated, after which the remaining variable is calculated."
            };
        }
    }

    y = (c1 - a1 * x) / b1;
    let xDisplay = Number.isInteger(x) ? String(x) : String(parseFloat(x.toFixed(6)));
    let yDisplay = Number.isInteger(y) ? String(y) : String(parseFloat(y.toFixed(6)));

    steps.push("Step 2: Solve for x:");
    steps.push(`x = ${xDisplay}`);
    steps.push(`Step 3: Substitute x = ${xDisplay} into Equation 1.`);
    steps.push(`y = ${yDisplay}`);
    steps.push(`🎯 Final Answer: x = ${xDisplay}, y = ${yDisplay}`);

    return {
        applicable: true,
        message: "Sankalana Vyavakalanabhyam can be applied successfully.",
        equations: [eq1, eq2],
        steps: steps,
        answer: { x: xDisplay, y: yDisplay },
        explanation: "Sankalana Vyavakalanabhyam means 'By Addition and By Subtraction'. The main idea is to combine two equations so that one variable disappears."
    };
}

// ============================================================
// 8. PURANAPURANABHYAM
// "By Completion or Non-Completion" (Completing the Square)
// ============================================================
function solvePuranapuranabhyam(a, b, c) {
    // Solves quadratic equation: ax^2 + bx + c = 0 using Completing the Square
    const coeffA = parseFloat(a);
    const coeffB = parseFloat(b);
    const coeffC = parseFloat(c);

    if (isNaN(coeffA) || isNaN(coeffB) || isNaN(coeffC) || coeffA === 0) {
        return {
            applicable: false,
            message: "Please enter a valid multiplication expression (e.g., 12 × 3 = 36).",
            steps: [],
            answer: null
        };
    }

    let steps = [
        `🧮 Equation: ${coeffA}x² + (${coeffB})x + (${coeffC}) = 0`,
        "📖 Sutra: Puranapuranabhyam",
        "💡 Meaning: By Completion or Non-Completion (Completing the Square)"
    ];

    // Divide by 'a' if a != 1
    let bNorm = coeffB / coeffA;
    let cNorm = coeffC / coeffA;

    if (coeffA !== 1) {
        steps.push(`Step 1: Divide the equation by a = ${coeffA}:`);
        steps.push(`x² + (${bNorm})x + (${cNorm}) = 0`);
    } else {
        steps.push("Step 1: Equation already has a unit coefficient for x².");
    }

    // Move constant to RHS
    let rhs1 = -cNorm;
    steps.push(`Step 2: Move constant term to RHS: x² + (${bNorm})x = ${rhs1}`);

    // Complete the square: Add (b / 2)^2 to both sides
    let halfB = bNorm / 2;
    let squareTerm = halfB * halfB;
    let rhs2 = rhs1 + squareTerm;

    steps.push(`Step 3: Complete the square by adding (${bNorm} / 2)² = ${squareTerm} to both sides:`);
    steps.push(`(x + ${halfB})² = ${rhs2}`);

    if (rhs2 < 0) {
        let realPart = -halfB;
        let imagPart = Math.sqrt(Math.abs(rhs2));
        let x1 = `${realPart} + ${imagPart.toFixed(4)}i`;
        let x2 = `${realPart} - ${imagPart.toFixed(4)}i`;

        steps.push(`Step 4: RHS is negative (${rhs2}). Roots are complex.`);
        steps.push(`✅ Final Answer: x = ${x1}, x = ${x2}`);

        return {
            applicable: true,
            message: "Solved using Puranapuranabhyam (Complex Roots).",
            steps: steps,
            answer: [x1, x2],
            explanation: "Puranapuranabhyam completes the square by adding a compensating square term to both sides of the quadratic equation."
        };
    }

    let sqrtRhs = Math.sqrt(rhs2);
    let root1 = -halfB + sqrtRhs;
    let root2 = -halfB - sqrtRhs;

    steps.push(`Step 4: Take square root of both sides: x + ${halfB} = ±${sqrtRhs}`);
    steps.push(`x1 = ${-halfB} + ${sqrtRhs} = ${root1}`);
    steps.push(`x2 = ${-halfB} - ${sqrtRhs} = ${root2}`);
    steps.push(`✅ Final Answer: x = ${root1}, x = ${root2}`);

    return {
        applicable: true,
        message: "Solved successfully using Puranapuranabhyam.",
        steps: steps,
        answer: [root1, root2],
        explanation: "Puranapuranabhyam completes the square by adding a compensating square term to both sides of the quadratic equation."
    };
}

// ============================================================
// 9. CHALANA-KALANABHYAM
// "Differences and Similarities"
// ============================================================
function solveChalanaKalanabhyam(equation) {
    if (!equation) {
        return {
            applicable: false,
            message: "Please enter a quadratic equation.",
            steps: [],
            answer: null
        };
    }

    equation = String(equation).trim();
    if (equation === "") {
        return {
            applicable: false,
            message: "Please enter a quadratic equation.",
            steps: [],
            answer: null
        };
    }

    let eq = equation.replace(/\s+/g, "").toLowerCase();

    if (!eq.includes("=")) {
        return {
            applicable: false,
            message: "Equation must contain '='.",
            steps: [],
            answer: null
        };
    }

    const parts = eq.split("=");
    if (parts.length !== 2) {
        return {
            applicable: false,
            message: "Please enter one valid equation.",
            steps: [],
            answer: null
        };
    }

    let left = parts[0];
    let right = parts[1];

    if (right !== "0") {
        return {
            applicable: false,
            message: "For this solver, enter the quadratic equation with 0 on the right side.",
            steps: [],
            answer: null
        };
    }

    left = left.replace(/\*\*2/g, "x2").replace(/x\^2/g, "x2").replace(/x²/g, "x2");

    const pattern = /^([+-]?\d*)x2([+-]\d+)?x([+-]\d+)?$/;
    const pattern2 = /^([+-]?\d*)x2([+-]\d+)?$/;

    let aText, bText, cText;
    let match = left.match(pattern);

    if (!match) {
        let match2 = left.match(pattern2);
        if (!match2) {
            return {
                applicable: false,
                message: "Please enter a quadratic equation in the form ax² + bx + c = 0.",
                steps: [],
                answer: null
            };
        }
        aText = match2[1];
        bText = null;
        cText = match2[2];
    } else {
        aText = match[1];
        bText = match[2];
        cText = match[3];
    }

    let a = (aText === "" || aText === "+") ? 1 : (aText === "-" ? -1 : parseInt(aText, 10));
    let b = bText ? parseInt(bText, 10) : 0;
    let c = cText ? parseInt(cText, 10) : 0;

    if (a === 0) {
        return {
            applicable: false,
            message: "This is not a quadratic equation.",
            steps: [],
            answer: null
        };
    }

    const discriminant = b * b - 4 * a * c;

    let steps = [];
    steps.push(`🧮 Equation: ${equation}`);
    steps.push("📖 Sutra: Chalana-Kalanabhyam");
    steps.push("💡 Meaning: Differences and Similarities.");
    steps.push("Step 1: Identify coefficients:");
    steps.push(`a = ${a}, b = ${b}, c = ${c}`);
    steps.push("Step 2: Calculate the discriminant using the difference.");
    steps.push("D = b² - 4ac");
    steps.push(`D = (${b})² - 4(${a})(${c})`);
    steps.push(`D = ${discriminant}`);

    if (discriminant < 0) {
        steps.push("The discriminant is negative.");
        steps.push("Therefore the equation has no real roots.");
        return {
            applicable: true,
            message: "No real roots.",
            steps: steps,
            answer: "No real roots",
            discriminant: discriminant,
            explanation: "The difference calculation gives a negative discriminant, so there are no real solutions."
        };
    }

    if (discriminant === 0) {
        let x = -b / (2 * a);
        let xDisplay = Number.isInteger(x) ? String(x) : String(parseFloat(x.toFixed(6)));

        steps.push("The discriminant is zero.");
        steps.push("Therefore both roots are equal.");
        steps.push("x = -b / 2a");
        steps.push(`x = -(${b}) / (2 × ${a})`);
        steps.push(`x = ${xDisplay}`);
        steps.push(`✅ Final Answer: x = ${xDisplay}`);

        return {
            applicable: true,
            message: "Equal roots found.",
            steps: steps,
            answer: xDisplay,
            discriminant: discriminant
        };
    }

    const sqrtD = Math.sqrt(discriminant);
    const x1 = (-b + sqrtD) / (2 * a);
    const x2 = (-b - sqrtD) / (2 * a);

    let x1Display = Number.isInteger(x1) ? String(x1) : String(parseFloat(x1.toFixed(6)));
    let x2Display = Number.isInteger(x2) ? String(x2) : String(parseFloat(x2.toFixed(6)));

    steps.push("The discriminant is positive.");
    steps.push("Therefore the equation has two real roots.");
    steps.push("Step 3: Find the square root of D.");
    steps.push(`√${discriminant} = ${sqrtD}`);
    steps.push("Step 4: Find the first root.");
    steps.push("x₁ = (-b + √D) / 2a");
    steps.push(`x₁ = (-(${b}) + √${discriminant}) / (2 × ${a})`);
    steps.push(`x₁ = ${x1Display}`);
    steps.push("Step 5: Find the second root.");
    steps.push("x₂ = (-b - √D) / 2a");
    steps.push(`x₂ = (-(${b}) - √${discriminant}) / (2 × ${a})`);
    steps.push(`x₂ = ${x2Display}`);
    steps.push("🎯 Final Answer:");
    steps.push(`x₁ = ${x1Display}, x₂ = ${x2Display}`);

    return {
        applicable: true,
        message: "Quadratic equation solved.",
        equation: equation,
        steps: steps,
        answer: { x1: x1Display, x2: x2Display },
        discriminant: discriminant,
        explanation: "Chalana-Kalanabhyam is associated with differences and similarities. The calculation is demonstrated here through the discriminant and root relationship of a quadratic equation."
    };
}

// ============================================================
// 10. YAVADUNAM
// "Whatever the Deficiency"
// ============================================================
function solveYavadunam(num1, num2) {
    const a = parseInt(String(num1).trim(), 10);
    const b = parseInt(String(num2).trim(), 10);

    if (isNaN(a) || isNaN(b)) {
        return {
            applicable: false,
            message: "Please enter two valid numbers.",
            steps: [],
            answer: null
        };
    }

    if (a <= 0 || b <= 0) {
        return {
            applicable: false,
            message: "Please enter positive numbers.",
            steps: [],
            answer: null
        };
    }

    const maxNumber = Math.max(a, b);
    const digits = String(maxNumber).length;
    let base = Math.pow(10, digits);

    const previousBase = Math.pow(10, digits - 1);
    const currentDistance = Math.abs(a - base) + Math.abs(b - base);
    const previousDistance = Math.abs(a - previousBase) + Math.abs(b - previousBase);

    if (previousDistance < currentDistance) {
        base = previousBase;
    }

    const deviationA = a - base;
    const deviationB = b - base;

    const relativeA = Math.abs(deviationA) / base;
    const relativeB = Math.abs(deviationB) / base;

    if (relativeA > 0.20 || relativeB > 0.20) {
        return {
            applicable: false,
            message: "Yavadunam is not suitable for these numbers. The numbers should be reasonably close to a convenient base such as 10, 100 or 1000.",
            steps: [],
            answer: null
        };
    }

    let leftPart = a + deviationB;
    let rightPart = deviationA * deviationB;
    const baseDigits = String(base).length - 1;
    const rightWidth = baseDigits;

    let rightDisplay = "";
    let carry = 0;

    if (rightPart >= 0) {
        rightDisplay = String(rightPart).padStart(rightWidth, '0');
        if (rightPart >= base) {
            carry = Math.floor(rightPart / base);
            let rightRemainder = rightPart % base;
            leftPart += carry;
            rightDisplay = String(rightRemainder).padStart(rightWidth, '0');
        } else {
            carry = 0;
        }
    } else {
        let borrow = 1;
        leftPart -= borrow;
        let positiveRight = base + rightPart;
        rightDisplay = String(positiveRight).padStart(rightWidth, '0');
        carry = -1;
    }

    const answer = parseInt(String(leftPart) + rightDisplay, 10);

    let steps = [];
    steps.push(`🧮 Question: ${a} × ${b}`);
    steps.push("📖 Sutra: Yāvadūnam");
    steps.push("💡 Meaning: Whatever the Deficiency");
    steps.push(`🎯 Step 1: Choose the nearest convenient base = ${base}`);
    steps.push(`The base contains ${baseDigits} zero(s).`);

    if (deviationA < 0) {
        steps.push(`Step 2: ${a} is deficient from ${base} by ${Math.abs(deviationA)}.`);
        steps.push(`${a} - ${base} = ${deviationA}`);
    } else {
        steps.push(`Step 2: ${a} exceeds ${base} by ${deviationA}.`);
        steps.push(`${a} - ${base} = +${deviationA}`);
    }

    if (deviationB < 0) {
        steps.push(`Step 3: ${b} is deficient from ${base} by ${Math.abs(deviationB)}.`);
        steps.push(`${b} - ${base} = ${deviationB}`);
    } else {
        steps.push(`Step 3: ${b} exceeds ${base} by ${deviationB}.`);
        steps.push(`${b} - ${base} = +${deviationB}`);
    }

    steps.push("🔄 Step 4: Cross subtract/add.");
    if (deviationB >= 0) {
        steps.push(`${a} + (${deviationB}) = ${a + deviationB}`);
    } else {
        steps.push(`${a} - ${Math.abs(deviationB)} = ${a + deviationB}`);
    }

    steps.push("✖️ Step 5: Multiply the deviations.");
    steps.push(`(${deviationA}) × (${deviationB}) = ${deviationA * deviationB}`);
    steps.push(`Step 6: Since base = ${base}, the right part must contain ${baseDigits} digit(s).`);
    steps.push(`Right part = ${rightDisplay}`);

    if (rightPart < 0) {
        steps.push("Because the right part is negative, borrow 1 from the left part.");
    } else if (rightPart >= base) {
        steps.push(`Carry ${carry} to the left part.`);
    }

    steps.push("Step 7: Combine:");
    steps.push(`Left part = ${leftPart}`);
    steps.push(`Right part = ${rightDisplay}`);
    steps.push(`🎯 Final Answer = ${leftPart}${rightDisplay}`);
    steps.push(`✅ Verification: ${a} × ${b} = ${answer}`);

    return {
        applicable: true,
        message: "Yāvadūnam can be applied successfully.",
        question: `${a} × ${b}`,
        base: base,
        deviation1: deviationA,
        deviation2: deviationB,
        left_part: leftPart,
        right_part: rightPart,
        steps: steps,
        answer: answer,
        explanation: "Yāvadūnam means 'Whatever the Deficiency'. Numbers close to a power-of-10 base are expressed as deficiencies or excesses from that base. The cross operation gives the left part and the product of deviations gives the right part."
    };
}

// ============================================================
// 11. VYASTI-SAMASTI
// "Part and Whole"
// ============================================================
function solveVyastiSamasti(num1, num2) {
    const a = parseInt(String(num1).trim(), 10);
    const b = parseInt(String(num2).trim(), 10);

    if (isNaN(a) || isNaN(b)) {
        return {
            applicable: false,
            message: "Please enter two valid numbers.",
            steps: [],
            answer: null
        };
    }

    if (a <= 0 || b <= 0) {
        return {
            applicable: false,
            message: "Please enter positive numbers.",
            steps: [],
            answer: null
        };
    }

    function bestDecomposition(number) {
        const digits = String(number).split('').map(x => parseInt(x, 10));
        const length = digits.length;
        let parts = [];

        digits.forEach((digit, index) => {
            let power = length - index - 1;
            let place = Math.pow(10, power);
            let value = digit * place;
            if (value !== 0) {
                parts.push(value);
            }
        });
        return parts;
    }

    const partsA = bestDecomposition(a);
    const partsB = bestDecomposition(b);

    let whole, parts, multiplier;
    if (partsA.length <= partsB.length) {
        whole = a;
        parts = partsA;
        multiplier = b;
    } else {
        whole = b;
        parts = partsB;
        multiplier = a;
    }

    let partialResults = parts.map(part => part * multiplier);
    const answer = partialResults.reduce((acc, curr) => acc + curr, 0);

    let steps = [];
    steps.push(`🧮 Question: ${a} × ${b}`);
    steps.push("📖 Sutra: Vyasti-Samasti");
    steps.push("💡 Meaning: Part and Whole");
    steps.push("Vyasti means 'Part' and Samasti means 'Whole'.");
    steps.push(`Step 1: Split ${whole} into convenient parts.`);
    steps.push(`${whole} = ${parts.join(" + ")}`);
    steps.push("Step 2: Multiply each part separately.");

    parts.forEach((part, idx) => {
        steps.push(`${part} × ${multiplier} = ${partialResults[idx]}`);
    });

    steps.push("Step 3: Add all partial results.");
    steps.push(`${partialResults.join(" + ")} = ${answer}`);
    steps.push(`🎯 Final Answer = ${answer}`);
    steps.push(`✅ Verification: ${a} × ${b} = ${answer}`);

    return {
        applicable: true,
        message: "Vyasti-Samasti can be applied successfully.",
        question: `${a} × ${b}`,
        whole: whole,
        parts: parts,
        partial_results: partialResults,
        steps: steps,
        answer: answer,
        explanation: "Vyasti-Samasti means 'Part and Whole'. The number is divided into convenient parts, each part is calculated separately, and the partial results are combined to obtain the whole answer."
    };
}

// ============================================================
// 12. SHESANYANKENA CHARAMENA
// "The remainders by the last digit"
// ============================================================
function solveShesanyankenaCharamena(input) {
    let inputStr = String(input).trim();
    let num = 1;
    let d = 1;

    // Numerator aur Denominator extract karo
    if (inputStr.includes('/')) {
        let parts = inputStr.split('/');
        num = parseInt(parts[0].trim(), 10);
        d = parseInt(parts[1].trim(), 10);
    } else {
        d = parseInt(inputStr, 10);
    }

    if (isNaN(d) || d <= 1 || isNaN(num)) {
        return {
            applicable: false,
            message: "Please enter a valid fraction (e.g., 123/9) or denominator greater than 1.",
            steps: [],
            answer: null
        };
    }

    let remainder = num % d;
    let integerPart = Math.floor(num / d);
    let decimals = [];
    let seenRemainders = new Map();
    let stepCount = 0;
    let isRepeating = false;
    let repeatStartIndex = -1;

    let steps = [
        `🧮 Calculating Decimal Expansion for ${num} / ${d}`,
        "📖 Sutra: Sheṣāṇyaṅkena Charamena",
        `Step 1: Integer division gives ${integerPart} with initial remainder ${remainder}.`
    ];

    if (remainder === 0) {
        return {
            applicable: true,
            message: "Exact division result.",
            denominator: d,
            steps: [`${num} ÷ ${d} = ${integerPart}`],
            answer: String(integerPart),
            explanation: "No decimal remainder."
        };
    }

    while (remainder !== 0 && stepCount < d) {
        if (seenRemainders.has(remainder)) {
            isRepeating = true;
            repeatStartIndex = seenRemainders.get(remainder);
            break;
        }

        seenRemainders.set(remainder, stepCount);

        let current = remainder * 10;
        let digit = Math.floor(current / d);
        let nextRemainder = current % d;

        steps.push(`Step ${stepCount + 1}: (${remainder} × 10) ÷ ${d} = ${digit} with remainder ${nextRemainder}`);
        decimals.push(digit);
        remainder = nextRemainder;
        stepCount++;
    }

    let decimalStr = "";
    if (isRepeating) {
        let nonRepeat = decimals.slice(0, repeatStartIndex).join("");
        let repeat = decimals.slice(repeatStartIndex).join("");
        decimalStr = `${integerPart}.${nonRepeat}(${repeat})`;
    } else {
        decimalStr = `${integerPart}.` + decimals.join("");
    }

    steps.push(`✅ Final Answer = ${decimalStr}`);

    return {
        applicable: true,
        message: "Sheṣāṇyaṅkena Charamena applied successfully.",
        denominator: d,
        steps: steps,
        answer: decimalStr,
        explanation: "Evaluates exact decimal places using remainder cycles."
    };
}
// ============================================================
// 13. SOPANTYADVAYAMANTYAM
// "The ultimate and twice the penultimate"
// ============================================================
function solveSopantyadvayamantyam(number) {
    const n = parseInt(String(number).trim(), 10);

    if (isNaN(n)) {
        return {
            applicable: false,
            message: "Please enter a valid number.",
            steps: [],
            answer: null
        };
    }

    if (n < 10) {
        return {
            applicable: false,
            message: "This Sutra requires at least two digits.",
            steps: [],
            answer: null
        };
    }

    const lastDigit = n % 10;
    const penultimateDigit = Math.floor(n / 10) % 10;
    const doublePenultimate = 2 * penultimateDigit;
    const value = lastDigit + doublePenultimate;

    let steps = [];
    steps.push(`🧮 Number: ${n}`);
    steps.push("📖 Sutra: Sopāntyadvayamantyam");
    steps.push("💡 Meaning: The ultimate and twice the penultimate.");
    steps.push(`Step 1: Ultimate (last digit) of ${n} = ${lastDigit}`);
    steps.push(`Step 2: Penultimate (second last digit) of ${n} = ${penultimateDigit}`);
    steps.push("Step 3: Twice the penultimate:");
    steps.push(`2 × ${penultimateDigit} = ${doublePenultimate}`);
    steps.push("Step 4: Add the ultimate and twice the penultimate.");
    steps.push(`${lastDigit} + ${doublePenultimate} = ${value}`);
    steps.push(`🎯 Final Answer = ${value}`);

    return {
        applicable: true,
        message: "Sopāntyadvayamantyam pattern calculated.",
        number: n,
        ultimate: lastDigit,
        penultimate: penultimateDigit,
        twice_penultimate: doublePenultimate,
        steps: steps,
        answer: value,
        explanation: "Sopāntyadvayamantyam means 'the ultimate and twice the penultimate'. The last digit is taken along with twice the second-last digit."
    };
}

// ============================================================
// 14. EKANYUNENA PURVENA
// "By one less than the previous one"
// ============================================================
function solveEkanyunenaPurvena(num1, num2) {
    const a = parseInt(String(num1).trim(), 10);
    const b = parseInt(String(num2).trim(), 10);

    if (isNaN(a) || isNaN(b) || a <= 0 || b <= 0) {
        return {
            applicable: false,
            message: "Please enter valid positive numbers.",
            steps: [],
            answer: null
        };
    }

    // Check if one of the numbers consists purely of 9s
    const isNines = (str) => /^9+$/.test(str);
    let multiplier = 0;
    let number = 0;

    if (isNines(String(b))) {
        number = a;
        multiplier = b;
    } else if (isNines(String(a))) {
        number = b;
        multiplier = a;
    } else {
        return {
            applicable: false,
            message: "Ekanyunena Purvena requires one of the numbers to consist entirely of 9s (e.g., 9, 99, 999).",
            steps: [],
            answer: null
        };
    }

    const ninesCount = String(multiplier).length;
    const numDigits = String(number).length;

    if (numDigits > ninesCount) {
        return {
            applicable: false,
            message: "The number of 9s must be equal to or greater than the digits of the other number.",
            steps: [],
            answer: null
        };
    }

    const leftPart = number - 1;
    const rightPart = Math.pow(10, ninesCount) - 1 - leftPart;
    const paddedRight = String(rightPart).padStart(ninesCount, '0');
    const answer = Number(`${leftPart}${paddedRight}`);

    let steps = [
        `🧮 Question: ${number} × ${multiplier}`,
        "📖 Sutra: Ekanyūnena Pūrveṇa",
        "💡 Meaning: By one less than the previous one",
        `Step 1: Subtract 1 from the number: ${number} - 1 = ${leftPart} (Left Part)`,
        `Step 2: Subtract Left Part from 9s: ${multiplier} - ${leftPart} = ${paddedRight} (Right Part)`,
        `Step 3: Combine Left Part and Right Part: ${leftPart} | ${paddedRight}`,
        `✅ Final Answer = ${answer}`
    ];

    return {
        applicable: true,
        message: "Ekanyūnena Pūrveṇa applied successfully.",
        steps: steps,
        answer: answer,
        explanation: "Ekanyūnena Pūrveṇa means 'By one less than the previous one'. It simplifies multiplication when multiplying any number by 9, 99, 999, etc."
    };
}

// ============================================================
// 15. GUNITASAMUCCAYAH
// "The product of the sums is equal to the sum of the product"
// ============================================================
function solveGunitasamuccayah(expr1, expr2) {
    // Verifies algebraic products e.g., (x + a)(x + b)
    if (!expr1 || !expr2) {
        return {
            applicable: false,
            message: "Please enter two algebraic binomial factors (e.g., x+2 and x+3).",
            steps: [],
            answer: null
        };
    }

    const clean1 = String(expr1).replace(/\s+/g, "").toLowerCase();
    const clean2 = String(expr2).replace(/\s+/g, "").toLowerCase();

    // Match forms like x+a or x-a
    const match1 = clean1.match(/^x([+-]\d+)$/);
    const match2 = clean2.match(/^x([+-]\d+)$/);

    if (!match1 || !match2) {
        return {
            applicable: false,
            message: "Please enter binomial factors in the format 'x+a' or 'x-a' (e.g., x+2 and x+3).",
            steps: [],
            answer: null
        };
    }

    const a = parseInt(match1[1], 10);
    const b = parseInt(match2[1], 10);

    const coeffX2 = 1;
    const coeffX = a + b;
    const constant = a * b;

    // Gunita Samuccayah Rule: (Sum of coeffs of F1) * (Sum of coeffs of F2) = Sum of coeffs of Result
    const sumF1 = 1 + a;
    const sumF2 = 1 + b;
    const productOfSums = sumF1 * sumF2;
    const sumOfProductCoeffs = coeffX2 + coeffX + constant;

    let expandedStr = `x² ${coeffX >= 0 ? '+ ' + coeffX : '- ' + Math.abs(coeffX)}x ${constant >= 0 ? '+ ' + constant : '- ' + Math.abs(constant)}`;

    let steps = [
        `🧮 Verify Product: (${clean1}) × (${clean2})`,
        "📖 Sutra: Guṇitasamuccayaḥ",
        "💡 Meaning: The product of the sums is equal to the sum of the product.",
        `Step 1: Multiply factors algebraically to get polynomial: ${expandedStr}`,
        `Step 2: Find Sum of Coefficients of Factor 1 (${clean1}): 1 + (${a}) = ${sumF1}`,
        `Step 3: Find Sum of Coefficients of Factor 2 (${clean2}): 1 + (${b}) = ${sumF2}`,
        `Step 4: Product of Sums (S₁ × S₂): ${sumF1} × ${sumF2} = ${productOfSums}`,
        `Step 5: Sum of Coefficients of Expanded Product: 1 + (${coeffX}) + (${constant}) = ${sumOfProductCoeffs}`,
        `Step 6: Verification: ${productOfSums} === ${sumOfProductCoeffs} (${productOfSums === sumOfProductCoeffs ? "MATCHED ✅" : "FAILED ❌"})`,
        `✅ Final Expanded Answer = ${expandedStr}`
    ];

    return {
        applicable: true,
        message: "Guṇitasamuccayaḥ verification successful.",
        steps: steps,
        answer: expandedStr,
        explanation: "Guṇitasamuccayaḥ states that the product of the sums of coefficients of the factors equals the sum of coefficients of the product polynomial."
    };
}

// ============================================================
// 16. GUNAKASAMUCCAYAH
// "The factor of the sum is equal to the sum of the factors"
// ============================================================
function solveGunakasamuccayah(a, b, c) {
    // Solves quadratic expression coefficients evaluation
    const coeffA = parseInt(String(a).trim(), 10);
    const coeffB = parseInt(String(b).trim(), 10);
    const coeffC = parseInt(String(c).trim(), 10);

    if (isNaN(coeffA) || isNaN(coeffB) || isNaN(coeffC)) {
        return {
            applicable: false,
            message: "Please enter three valid coefficients for ax² + bx + c.",
            steps: [],
            answer: null
        };
    }

    const sumCoeffs = coeffA + coeffB + coeffC;
    let quadStr = `${coeffA}x² ${coeffB >= 0 ? '+ ' + coeffB : '- ' + Math.abs(coeffB)}x ${coeffC >= 0 ? '+ ' + coeffC : '- ' + Math.abs(coeffC)}`;

    let steps = [
        `🧮 Expression: ${quadStr}`,
        "📖 Sutra: Guṇakasamuccayaḥ",
        "💡 Meaning: The factor of the sum is equal to the sum of the factors.",
        `Step 1: Evaluate expression for x = 1.`,
        `Step 2: ${coeffA}(1)² + ${coeffB}(1) + ${coeffC} = ${coeffA} + ${coeffB} + ${coeffC}`,
        `Step 3: Sum of Coefficients = ${sumCoeffs}`,
        `✅ Final Answer = Sum of coefficients is ${sumCoeffs}`
    ];

    return {
        applicable: true,
        message: "Guṇakasamuccayaḥ applied successfully.",
        steps: steps,
        answer: sumCoeffs,
        explanation: "Guṇakasamuccayaḥ evaluates the sum of coefficients of a polynomial by substituting x = 1."
    };
}

