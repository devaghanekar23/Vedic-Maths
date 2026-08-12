// ==========================================
// VEDIC MATHEMATICS SPEED TEST
// speed.js
// ==========================================


// ================= QUESTIONS =================


const questions = [

{
q:"25² = ?",
a:625
},

{
q:"35² = ?",
a:1225
},

{
q:"45² = ?",
a:2025
},

{
q:"55² = ?",
a:3025
},

{
q:"65² = ?",
a:4225
},

{
q:"75² = ?",
a:5625
},

{
q:"23 × 12 = ?",
a:276
},

{
q:"34 × 21 = ?",
a:714
},

{
q:"45 × 11 = ?",
a:495
},

{
q:"98 × 97 = ?",
a:9506
},

{
q:"99 × 99 = ?",
a:9801
},

{
q:"125 + 375 = ?",
a:500
},

{
q:"567 + 234 = ?",
a:801
},

{
q:"999 - 456 = ?",
a:543
},

{
q:"888 - 333 = ?",
a:555
},

{
q:"12 × 12 = ?",
a:144
},

{
q:"15 × 15 = ?",
a:225
},

{
q:"16 × 16 = ?",
a:256
},

{
q:"24 × 25 = ?",
a:600
},

{
q:"50 × 50 = ?",
a:2500
},

{
q:"101 × 99 = ?",
a:9999
},

{
q:"111 × 11 = ?",
a:1221
},

{
q:"75 + 125 = ?",
a:200
},

{
q:"1000 - 675 = ?",
a:325
},

{
q:"72 ÷ 8 = ?",
a:9
}

];





// ================= VARIABLES =================


let currentAnswer = 0;

let score = 0;

let count = 0;

let correct = 0;

let wrong = 0;

let time = 30;

let timer;

let started = false;






// ================= START TEST =================


function startTest(){



if(started)
{
return;
}



started = true;


score = 0;

count = 0;

correct = 0;

wrong = 0;

time = 30;



document.getElementById("score").innerHTML = 0;

document.getElementById("count").innerHTML = 0;

document.getElementById("timer").innerHTML = time;



document.getElementById("answer").disabled = false;

document.getElementById("submitBtn").disabled = false;

document.getElementById("startBtn").disabled = true;



document.getElementById("result").innerHTML="";



showQuestion();





timer = setInterval(function(){



time--;



document.getElementById("timer").innerHTML = time;



if(time <= 0)
{

endTest();

}



},1000);



}







// ================= SHOW QUESTION =================


function showQuestion(){



let random = Math.floor(
Math.random()*questions.length
);



currentAnswer = questions[random].a;



document.getElementById("question").innerHTML =

"🧮 " + questions[random].q;



document.getElementById("answer").value="";



}







// ================= CHECK ANSWER =================


function checkAnswer(){



if(!started)
{

alert("Start the test first!");

return;

}



let input =
document.getElementById("answer").value;



if(input==="")
{

return;

}



let userAnswer =
Number(input);



count++;




if(userAnswer === currentAnswer)
{


score++;

correct++;


}

else
{


wrong++;


}





document.getElementById("score").innerHTML =
score;



document.getElementById("count").innerHTML =
count;



showQuestion();



}







// ================= END TEST =================


function endTest(){



clearInterval(timer);



started=false;



document.getElementById("answer").disabled=true;

document.getElementById("submitBtn").disabled=true;



document.getElementById("startBtn").disabled=false;



document.getElementById("question").innerHTML =

"🏆 Test Completed";





let accuracy = 0;



if(count>0)
{

accuracy =
Math.round(
(correct/count)*100
);

}






let bestScore =
localStorage.getItem("bestScore") || 0;



if(score > bestScore)
{

localStorage.setItem(
"bestScore",
score
);


bestScore = score;


}






document.getElementById("result").innerHTML = `


<div class="alert alert-success">


<h3>
🎉 Speed Test Result
</h3>



<p>
✅ Correct Answers :
<b>${correct}</b>
</p>


<p>
❌ Wrong Answers :
<b>${wrong}</b>
</p>


<p>
📚 Total Questions :
<b>${count}</b>
</p>


<p>
🎯 Accuracy :
<b>${accuracy}%</b>
</p>


<p>
🏆 Best Score :
<b>${bestScore}</b>
</p>



<button 
onclick="restartTest()"
class="btn btn-primary">

Restart Test

</button>



</div>

`;



}







// ================= RESTART =================


function restartTest(){


location.reload();


}







// ================= ENTER KEY =================


document.addEventListener(
"keydown",
function(event){


if(event.key==="Enter")
{


checkAnswer();


}


});