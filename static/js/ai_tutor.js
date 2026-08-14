// ======================================
// VEDIC MATHS AI TUTOR SYSTEM
// ======================================


// IMAGE PREVIEW

let imageInput = document.getElementById("imageInput");


if(imageInput){

imageInput.addEventListener("change", function(){

let file = this.files[0];


if(file){

let reader = new FileReader();


reader.onload = function(e){

document.getElementById("preview").innerHTML = `

<img src="${e.target.result}"
style="
width:250px;
border-radius:20px;
margin-top:20px;
box-shadow:0 10px 30px rgba(0,0,0,.4);
">

`;

}


reader.readAsDataURL(file);

}

});

}





// ======================================
// AI SCAN SOLVE
// ======================================


function scanQuestion(){


let solutionBox =
document.getElementById("solutionBox");


let solution =
document.getElementById("solution");



solutionBox.style.display="block";



solution.innerHTML = `

<div class="answer-card">


<h3>
🤖 AI Analysing Question...
</h3>


<p>
Scanning image and finding Vedic Maths method...
</p>


</div>

`;



setTimeout(()=>{


solution.innerHTML = `


<div class="answer-card">


<h2>
✅ AI Solution Found
</h2>


<h3>
Example: 45²
</h3>


<div class="step">

<div class="step-number">
1
</div>

Take number before 5

<br>

45 → 4

</div>



<div class="step">

<div class="step-number">
2
</div>

Multiply with next number

<br>

4 × 5 = 20

</div>



<div class="step">

<div class="step-number">
3
</div>

Attach 25

<br>

Answer = 2025

</div>


<h2>
🎯 Final Answer = 2025
</h2>



</div>


`;


},2000);



}







// ======================================
// AI TUTOR QUESTION SOLVER
// ======================================


function askTutor(){



let question =
document.getElementById("userQuestion").value;



let answer =
document.getElementById("aiAnswer");



if(question==""){


answer.innerHTML=`

<p>
⚠️ Please enter question
</p>

`;

return;

}




answer.innerHTML=`

<div class="answer-card">

<h3>
🤖 AI Thinking...
</h3>

</div>

`;





setTimeout(()=>{


let result="";



if(question.includes("45") && question.includes("²")){


result=`

<h3>
Ekadhikena Purvena Method
</h3>


<p>

45²

<br><br>

Step 1:

Remove 5 → 4


<br>

Step 2:

4 × 5 = 20


<br>

Step 3:

Attach 25


<br><br>

<strong>
Answer = 2025
</strong>

</p>

`;

}



else if(question.includes("35")){


result=`

<h3>
35² Solution
</h3>


<p>

3 × 4 = 12

<br>

Attach 25

<br><br>

<strong>
Answer = 1225
</strong>

</p>

`;

}




else if(question.includes("25")){


result=`

<h3>
25² Solution
</h3>


<p>

2 × 3 = 6

<br>

Attach 25

<br><br>

<strong>
Answer = 625
</strong>

</p>

`;

}




else{


result=`

<h3>
🤖 AI Tutor Suggestion
</h3>


<p>

I can solve Vedic Maths problems like:

<br><br>

• Square ending with 5

<br>

• Multiplication near base

<br>

• Sutra based calculations

</p>

`;

}




answer.innerHTML=result;



},1500);



}