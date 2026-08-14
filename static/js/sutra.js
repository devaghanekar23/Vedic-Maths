/* =====================================
      VEDIC MATHEMATICS SUTRA JS
===================================== */


/* =====================================
      EKADHIKENA PURVENA
      Square Ending With 5
===================================== */


function calculateSquare(){

    let input = document.getElementById("vedicNumber");
    let result = document.getElementById("squareResult");


    if(!input || !result){
        return;
    }


    let number = parseInt(input.value);


    if(isNaN(number)){

        result.innerHTML = `
        <div class="alert alert-danger mt-3">
        ⚠️ Please enter a number
        </div>
        `;

        return;
    }


    if(number % 10 !== 5){

        result.innerHTML = `
        <div class="alert alert-danger mt-3">
        ❌ Please enter number ending with 5
        </div>
        `;

        return;
    }



    let first = Math.floor(number / 10);

    let second = first + 1;

    let multiplication = first * second;

    let answer = multiplication + "25";



    result.innerHTML = `

    <div class="answer-card">

    <h2>
    🎉 Final Answer = ${answer}
    </h2>


    <div class="step">

    <b>Step 1:</b>

    <br>

    Remove last digit 5

    <br>

    ${number} → ${first}

    </div>



    <div class="step">

    <b>Step 2:</b>

    <br>

    ${first} × ${second}

    = ${multiplication}

    </div>



    <div class="step">

    <b>Step 3:</b>

    <br>

    Add 25 at the end

    </div>


    <div class="alert alert-success mt-3">

    Formula:

    <br>

    <b>
    n5² = n × (n+1) followed by 25
    </b>

    </div>


    </div>

    `;

}






/* =====================================
      NIKHILAM NAVATASHCARAMAM DASHATAH
      Multiplication Near Base 100
===================================== */


function calculateNikhilam(){


    let num1Input = document.getElementById("num1");

    let num2Input = document.getElementById("num2");

    let result = document.getElementById("nikhilamResult");



    if(!num1Input || !num2Input || !result){
        return;
    }



    let num1 = parseInt(num1Input.value);

    let num2 = parseInt(num2Input.value);



    if(isNaN(num1) || isNaN(num2)){


        result.innerHTML = `

        <div class="alert alert-danger">

        ⚠️ Enter both numbers

        </div>

        `;

        return;

    }



    let base = 100;



    let deficiency1 = base - num1;

    let deficiency2 = base - num2;



    let leftPart = num1 - deficiency2;


    let rightPart = deficiency1 * deficiency2;


    let rightDisplay = rightPart.toString().padStart(2,"0");



    let answer = leftPart + rightDisplay;



    result.innerHTML = `


    <div class="answer-card">


    <h2>
    🎉 Final Answer = ${answer}
    </h2>



    <div class="step">

    <b>Step 1: Base</b>

    <br>

    Base = ${base}

    </div>




    <div class="step">

    <b>Step 2: Deficiency</b>

    <br>

    ${num1} → ${deficiency1} less

    <br>

    ${num2} → ${deficiency2} less

    </div>




    <div class="step">

    <b>Step 3: Cross Subtraction</b>

    <br>

    ${num1} - ${deficiency2}

    = ${leftPart}

    </div>




    <div class="step">

    <b>Step 4: Deficiency Multiplication</b>

    <br>

    ${deficiency1} × ${deficiency2}

    = ${rightDisplay}

    </div>



    <div class="alert alert-success mt-3">

    Formula:

    <br>

    <b>
    (Base - Deficiency Method)
    </b>

    </div>



    </div>


    `;


}
function calculateUrdhva(){

let num1 = parseInt(
document.getElementById("urdhvaNum1").value
);

let num2 = parseInt(
document.getElementById("urdhvaNum2").value
);

let result = document.getElementById("urdhvaResult");


if(isNaN(num1) || isNaN(num2)){

result.innerHTML = `
<div class="alert alert-danger">
⚠️ Enter both numbers
</div>
`;

return;

}


let a = Math.floor(num1/10);
let b = num1 % 10;

let c = Math.floor(num2/10);
let d = num2 % 10;


let step1 = b*d;

let step2 = (a*d)+(b*c);

let step3 = a*c;


let answer = num1*num2;



result.innerHTML = `

<div class="answer-card">

<h2>
🎉 Final Answer = ${answer}
</h2>

<hr>

<div class="step">

<b>Step 1: Vertical Multiplication</b>

<br>

${b} × ${d} = ${step1}

</div>


<div class="step">

<b>Step 2: Crosswise Multiplication</b>

<br>

(${a}×${d}) + (${b}×${c})

<br>

= ${step2}

</div>


<div class="step">

<b>Step 3: Vertical Multiplication</b>

<br>

${a} × ${c} = ${step3}

</div>


<div class="alert alert-success mt-3">

Formula:

<br>

<b>
Vertical and Crosswise Method
</b>

</div>


</div>

`;

}
// =====================================
// PARAVARTYA YOJAYET
// Transpose and Apply Division
// =====================================


function calculateParavartya(){


let dividend = parseInt(
document.getElementById("dividend").value
);


let divisor = parseInt(
document.getElementById("divisor").value
);



let result = document.getElementById("paravartyaResult");



if(isNaN(dividend) || isNaN(divisor)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both numbers

</div>

`;

return;

}



if(divisor == 0){


result.innerHTML = `

<div class="alert alert-danger">

❌ Division by zero not possible

</div>

`;

return;

}



let quotient = Math.floor(dividend/divisor);

let remainder = dividend % divisor;



result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Quotient = ${quotient}

</h2>



<hr>



<div class="step">


<b>Step 1: Given Numbers</b>

<br>

Dividend = ${dividend}

<br>

Divisor = ${divisor}


</div>




<div class="step">


<b>Step 2: Apply Paravartya Yojayet</b>

<br>

Transpose the divisor digits

<br>

and apply calculation method.


</div>




<div class="step">


<b>Step 3: Division Result</b>

<br>

${dividend} ÷ ${divisor}

<br>

= ${quotient}

</div>




<div class="step">


<b>Remainder</b>

<br>

${remainder}

</div>



<div class="alert alert-success mt-3">


Formula:

<br>


<b>

Paravartya Yojayet = Transpose and Apply

</b>


</div>



</div>


`;

}
// =====================================
// SHUNYAM SAAMYASAMUCCAYE
// Common Sum Rule
// =====================================


function calculateShunyam(){


let a = parseInt(
document.getElementById("s1").value
);


let b = parseInt(
document.getElementById("s2").value
);


let c = parseInt(
document.getElementById("s3").value
);


let d = parseInt(
document.getElementById("s4").value
);



let result =
document.getElementById("shunyamResult");



if(isNaN(a)||isNaN(b)||isNaN(c)||isNaN(d)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter all values

</div>

`;

return;

}




let sum1 = a+b;

let sum2 = c+d;



if(sum1 == sum2){


result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Common Sum Found

</h2>


<hr>


<div class="step">


<b>Step 1:</b>

<br>

First Side:

${a} + ${b}

=

${sum1}


</div>




<div class="step">


<b>Step 2:</b>

<br>

Second Side:

${c} + ${d}

=

${sum2}


</div>




<div class="alert alert-success mt-3">


Formula:

<br>


<b>

When the sum is same, the result is zero

</b>


</div>



</div>


`;



}

else{


result.innerHTML = `


<div class="alert alert-warning">


❌ Common Sum Not Found


<br>


${a}+${b} = ${sum1}

<br>

${c}+${d} = ${sum2}


</div>


`;

}


}
// =====================================
// ANURUPYENA
// Proportionately Method
// =====================================


function calculateAnurupyena(){


let number = parseInt(
document.getElementById("anuNumber").value
);


let ratio = parseInt(
document.getElementById("anuRatio").value
);



let result =
document.getElementById("anurupyenaResult");



if(isNaN(number) || isNaN(ratio)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter number and ratio

</div>

`;

return;

}



let answer = number * ratio;



result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Final Answer = ${answer}

</h2>



<hr>



<div class="step">


<b>Step 1: Given Number</b>


<br>


Number = ${number}


</div>




<div class="step">


<b>Step 2: Apply Proportion</b>


<br>


${number} × ${ratio}


</div>




<div class="step">


<b>Step 3: Calculation</b>


<br>


${number} × ${ratio}

=

${answer}


</div>




<div class="alert alert-success mt-3">


Formula:

<br>


<b>

Value × Proportion = Result

</b>


</div>



</div>


`;

}
// =====================================
// SANKALANA VYAVAKALANABHYAM
// Addition and Subtraction
// =====================================


function calculateSankalana(){


let num1 = parseInt(
document.getElementById("sankNum1").value
);


let num2 = parseInt(
document.getElementById("sankNum2").value
);



let result =
document.getElementById("sankalanaResult");



if(isNaN(num1) || isNaN(num2)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both numbers

</div>

`;

return;

}



let addition = num1 + num2;


let subtraction = num1 - num2;



result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Calculation Complete

</h2>



<hr>



<div class="step">


<b>Step 1: Sankalana (Addition)</b>


<br>


${num1} + ${num2}


=

${addition}


</div>




<div class="step">


<b>Step 2: Vyavakalanam (Subtraction)</b>


<br>


${num1} - ${num2}


=

${subtraction}


</div>




<div class="alert alert-success mt-3">


Formula:

<br>


<b>

Sankalana = Addition

<br>

Vyavakalanam = Subtraction

</b>


</div>



</div>


`;

}
/* =====================================
   PURANAPURANABHYAM
   Completion Method
===================================== */


function calculatePuranapuranabhyam(){


let num1 =
parseInt(document.getElementById("puranNum1").value);


let num2 =
parseInt(document.getElementById("puranNum2").value);



let result =
document.getElementById("puranResult");



if(isNaN(num1) || isNaN(num2)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both numbers

</div>

`;

return;

}



let base = Math.ceil(num1/10)*10;


let difference = base - num1;


let remaining = num2 - difference;


let answer = base + remaining;



result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Final Answer = ${answer}

</h2>


<hr>



<div class="step">

<b>Step 1: Choose Base</b>

<br>

Base = ${base}

</div>



<div class="step">

<b>Step 2: Complete First Number</b>

<br>

${num1} + ${difference} = ${base}

</div>



<div class="step">

<b>Step 3: Adjust Second Number</b>

<br>

${num2} - ${difference}

=

${remaining}

</div>



<div class="step">

<b>Step 4: Final</b>

<br>

${base} + ${remaining}

=

${answer}

</div>



<div class="alert alert-success mt-3">


Formula:

<br>


<b>

Completion + Adjustment Method

</b>


</div>


</div>


`;

}
/* =====================================
   CHALANA KALANABHYAM
   Difference Method
===================================== */


function calculateChalana(){


let a = parseInt(
document.getElementById("chalanaA").value
);


let b = parseInt(
document.getElementById("chalanaB").value
);



let result =
document.getElementById("chalanaResult");



if(isNaN(a) || isNaN(b)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both numbers

</div>

`;

return;

}





let sum = a + b;


let difference = a - b;


let answer = sum * difference;




result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Final Answer = ${answer}

</h2>



<hr>



<div class="step">


<b>Step 1: Apply Formula</b>


<br>


a² - b² = (a+b)(a-b)


</div>




<div class="step">


<b>Step 2: Add Values</b>


<br>


${a} + ${b} = ${sum}


</div>




<div class="step">


<b>Step 3: Find Difference</b>


<br>


${a} - ${b} = ${difference}


</div>




<div class="step">


<b>Step 4: Multiply</b>


<br>


${sum} × ${difference}

=

${answer}


</div>




<div class="alert alert-success mt-3">


Formula:

<br>


<b>

(a+b)(a-b)

</b>


</div>



</div>


`;

}
/* =====================================
   YAVADUNAM
   Deficiency Method
===================================== */


function calculateYavadunam(){


let num1 = parseInt(
document.getElementById("yavadNum1").value
);


let num2 = parseInt(
document.getElementById("yavadNum2").value
);



let result =
document.getElementById("yavadResult");



if(isNaN(num1) || isNaN(num2)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both numbers

</div>

`;

return;

}



let base = 100;


let def1 = base - num1;

let def2 = base - num2;



let left = num1 - def2;


let right = def1 * def2;



if(right < 10){

right = "0" + right;

}



let answer = left * base + Number(right);



result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Final Answer = ${answer}

</h2>


<hr>



<div class="step">

<b>Step 1: Base</b>

<br>

Base = ${base}

</div>



<div class="step">

<b>Step 2: Deficiency</b>

<br>

${num1} → ${def1}

<br>

${num2} → ${def2}

</div>



<div class="step">

<b>Step 3: Cross Subtraction</b>

<br>

${num1} - ${def2}

=

${left}

</div>



<div class="step">

<b>Step 4: Multiply Deficiency</b>

<br>

${def1} × ${def2}

=

${right}

</div>



<div class="alert alert-success mt-3">

Formula:

<br>

<b>

Base - Deficiency Method

</b>

</div>



</div>


`;

}
/* =====================================
   VYASTISAMANSTIH
   Part and Whole Method
===================================== */


function calculateVyasti(){


let part1 = parseInt(
document.getElementById("vyastiNum1").value
);


let part2 = parseInt(
document.getElementById("vyastiNum2").value
);



let result =
document.getElementById("vyastiResult");



if(isNaN(part1) || isNaN(part2)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both values

</div>

`;

return;

}




let whole = part1 + part2;



result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Whole Value = ${whole}

</h2>


<hr>



<div class="step">


<b>Step 1: Identify Parts</b>


<br>


Part 1 = ${part1}

<br>

Part 2 = ${part2}


</div>




<div class="step">


<b>Step 2: Combine Parts</b>


<br>


${part1} + ${part2}

=

${whole}


</div>




<div class="alert alert-success mt-3">


Formula:

<br>


<b>

Whole = Part 1 + Part 2

</b>


</div>



</div>


`;

}
function calculateShesanyankena(){


let number = parseInt(
document.getElementById("remainderNumber").value
);


let divisor = parseInt(
document.getElementById("remainderDivisor").value
);


let result = document.getElementById("remainderResult");



if(isNaN(number) || isNaN(divisor)){


result.innerHTML = `
<div class="alert alert-danger">
⚠️ Enter both values
</div>
`;

return;

}



let remainder = number % divisor;



result.innerHTML = `

<div class="answer-card">

<h2>
🎉 Remainder = ${remainder}
</h2>


<p>
${number} ÷ ${divisor}
</p>


<p>
Remaining Value = ${remainder}
</p>


</div>

`;

}
/* =====================================
   SOPANTYADVAYAMANTYAM
   Factorization Method
===================================== */


function calculateSopantya(){


let a = parseInt(
document.getElementById("factorA").value
);


let b = parseInt(
document.getElementById("factorB").value
);


let c = parseInt(
document.getElementById("factorC").value
);



let result = document.getElementById("sopantyaResult");



if(isNaN(a) || isNaN(b) || isNaN(c)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter all values

</div>

`;

return;

}




let product = a*c;


let factors = [];



for(let i=-Math.abs(product); i<=Math.abs(product); i++){


    if(i !== 0 && product % i === 0){

        factors.push(i);

    }

}



result.innerHTML = `


<div class="answer-card">


<h2>
🎉 Factorization Result
</h2>


<hr>


<div class="step">

<b>Given:</b>

<br>

${a}x² + ${b}x + ${c}

</div>



<div class="step">

<b>Product:</b>

<br>

a × c = ${product}

</div>



<div class="step">

<b>Possible Factors:</b>

<br>

${factors.join(", ")}

</div>



<div class="alert alert-success mt-3">

Formula:

<br>

<b>
Ultimate and Twice the Penultimate Rule
</b>

</div>



</div>


`;

}
/* =====================================
   EKANYUNENA PURVENA
   Multiplication Near Base
===================================== */


function calculateEkanyunena(){


let num1 = parseInt(
document.getElementById("ekanyuNum1").value
);


let num2 = parseInt(
document.getElementById("ekanyuNum2").value
);



let result = document.getElementById("ekanyuResult");



if(isNaN(num1) || isNaN(num2)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter both numbers

</div>

`;

return;

}




let base = 100;



let diff1 = base - num1;

let diff2 = base - num2;



let left = num1 - diff2;


let right = diff1 * diff2;



let answer = left * base + right;



result.innerHTML = `


<div class="answer-card">


<h2>
🎉 Final Answer = ${answer}
</h2>


<hr>



<div class="step">

<b>Step 1: Base</b>

<br>

Base = ${base}

</div>




<div class="step">

<b>Step 2: Deficiency</b>

<br>

${num1} → ${diff1} less

<br>

${num2} → ${diff2} less

</div>




<div class="step">

<b>Step 3: Subtraction</b>

<br>

${num1} - ${diff2}

=

${left}

</div>




<div class="step">

<b>Step 4: Multiply Deficiency</b>

<br>

${diff1} × ${diff2}

=

${right}

</div>




<div class="alert alert-success mt-3">

Formula:

<br>

<b>

One less than previous number

</b>

</div>



</div>


`;

}
/* =====================================
   GUNITASAMUCHYAH
   Multiplication Verification
===================================== */


function calculateGunitasamuchyah(){


let num1 = parseInt(
document.getElementById("gunitNum1").value
);


let num2 = parseInt(
document.getElementById("gunitNum2").value
);



let userAnswer = parseInt(
document.getElementById("gunitAnswer").value
);



let result = document.getElementById("gunitResult");



if(isNaN(num1) || isNaN(num2) || isNaN(userAnswer)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter all values

</div>

`;

return;

}




let actualAnswer = num1 * num2;



let sum1 = digitSum(num1);

let sum2 = digitSum(num2);

let sumAnswer = digitSum(userAnswer);




let check = digitSum(actualAnswer);




let status = "";



if(actualAnswer === userAnswer){

status = "✅ Correct Multiplication";

}

else{

status = "❌ Wrong Answer";

}





result.innerHTML = `


<div class="answer-card">


<h2>
${status}
</h2>


<hr>



<div class="step">

<b>Actual Answer:</b>

<br>

${num1} × ${num2} = ${actualAnswer}

</div>




<div class="step">

<b>Digit Sum Check:</b>

<br>

${sum1} × ${sum2}

</div>



<div class="step">

Your Answer Digit Sum:

<br>

${sumAnswer}

</div>




<div class="alert alert-success mt-3">

Formula:

<br>

<b>

Product of Sum = Sum of Product

</b>

</div>



</div>


`;



}




function digitSum(number){


let sum = 0;


while(number > 0){

sum += number % 10;

number = Math.floor(number / 10);

}


return sum;

}
/* =====================================
   GUNAKASAMUCHYAH
   Factor Sum Method
===================================== */


function calculateGunakasamuchyah(){


let number = parseInt(
document.getElementById("gunaNumber").value
);


let result = document.getElementById("gunaResult");



if(isNaN(number)){


result.innerHTML = `

<div class="alert alert-danger">

⚠️ Enter a number

</div>

`;

return;

}



let factors = [];

let sum = 0;



for(let i = 1; i <= number; i++){


    if(number % i === 0){

        factors.push(i);

        sum += i;

    }

}




result.innerHTML = `


<div class="answer-card">


<h2>

🎉 Factor Sum = ${sum}

</h2>


<hr>



<div class="step">


<b>Number:</b>

<br>

${number}

</div>




<div class="step">


<b>Factors:</b>

<br>

${factors.join(" + ")}

</div>




<div class="step">


<b>Total Sum:</b>

<br>

${sum}

</div>




<div class="alert alert-success mt-3">


Formula:

<br>


<b>

Sum of Factors Method

</b>


</div>



</div>


`;



}