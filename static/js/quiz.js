// ==================================================
// VEDIC MATHEMATICS PROFESSIONAL QUIZ SYSTEM
// quiz.js (FIXED + LIVE DB SAVING)
// ==================================================

// Ye quiz_id backend ke /quiz route mein bhi 1 hardcoded hai.
// Dono jagah same rehna chahiye.
const QUIZ_ID = 1;

// ================= QUESTIONS DATABASE =================
// (Part 1 ke 30 + pehle comment mein chhupe hue Part 2 ke
//  25 questions - ab dono properly array mein hain = 55 total)

const questions = [

  { question:"Who is known as the father of Vedic Mathematics?",
    options:["Brahmagupta","Bharati Krishna Tirthaji","Aryabhata","Ramanujan"],
    answer:"Bharati Krishna Tirthaji" },

  { question:"How many main Sutras are there in Vedic Mathematics?",
    options:["10","12","16","20"],
    answer:"16" },

  { question:"How many Sub-Sutras are present in Vedic Mathematics?",
    options:["8","13","16","20"],
    answer:"13" },

  { question:"Vedic Mathematics is based on which ancient Indian knowledge system?",
    options:["Vedas","Physics","Astronomy","Medicine"],
    answer:"Vedas" },

  { question:"The word 'Vedic' is derived from which word?",
    options:["Veda","Vidya","Vishwa","Vigyan"],
    answer:"Veda" },

  { question:"Which Sutra means 'All from 9 and last from 10'?",
    options:["Nikhilam Navatashcaramam Dashatah","Ekadhikena Purvena","Paravartya Yojayet","Anurupyena"],
    answer:"Nikhilam Navatashcaramam Dashatah" },

  { question:"Which Sutra is used for multiplication?",
    options:["Urdhva Tiryagbhyam","Sunyam Saamyasamuccaye","Shunyam Anyat","Yavadunam"],
    answer:"Urdhva Tiryagbhyam" },

  { question:"Urdhva Tiryagbhyam means:",
    options:["Vertically and Crosswise","One more than previous","By addition","By subtraction"],
    answer:"Vertically and Crosswise" },

  { question:"Which Sutra is useful for numbers near a base?",
    options:["Nikhilam","Ekadhikena","Paravartya","Vyasti Samasti"],
    answer:"Nikhilam" },

  { question:"Ekadhikena Purvena means:",
    options:["By one more than previous one","All from 9","Vertically crosswise","Transpose and adjust"],
    answer:"By one more than previous one" },

  { question:"Who wrote the book 'Vedic Mathematics'?",
    options:["Bharati Krishna Tirthaji","Bhaskara","Aryabhata","Euclid"],
    answer:"Bharati Krishna Tirthaji" },

  { question:"Vedic Mathematics mainly helps to improve:",
    options:["Drawing skills","Calculation speed","Programming","Typing speed"],
    answer:"Calculation speed" },

  { question:"Which method is famous for fast multiplication?",
    options:["Urdhva Tiryagbhyam","Long division","Tables","Counting"],
    answer:"Urdhva Tiryagbhyam" },

  { question:"Paravartya Yojayet means:",
    options:["Transpose and apply","Multiply directly","Add numbers","Divide equally"],
    answer:"Transpose and apply" },

  { question:"Vedic Mathematics makes calculations:",
    options:["Slow","Complicated","Fast and simple","Impossible"],
    answer:"Fast and simple" },

  { question:"Which Sutra is related to squaring numbers ending with 5?",
    options:["Ekadhikena Purvena","Nikhilam","Paravartya","Anurupyena"],
    answer:"Ekadhikena Purvena" },

  { question:"The base method is commonly used with:",
    options:["Numbers close to powers of 10","Fractions only","Letters","Graphs"],
    answer:"Numbers close to powers of 10" },

  { question:"100 - 98 calculation is based on:",
    options:["Base concept","Division","Addition","Subtraction only"],
    answer:"Base concept" },

  { question:"Vedic Mathematics was introduced to the world in:",
    options:["20th century","15th century","10th century","5th century"],
    answer:"20th century" },

  { question:"Which operation can be solved quickly using Vedic methods?",
    options:["Multiplication","Only addition","Only subtraction","Only counting"],
    answer:"Multiplication" },

  { question:"The main aim of Vedic Mathematics is:",
    options:["Complex calculations","Mental calculation speed","Writing formulas","Computer programming"],
    answer:"Mental calculation speed" },

  { question:"Which Sutra is known as 'Vertically and Crosswise'?",
    options:["Urdhva Tiryagbhyam","Nikhilam","Ekadhikena","Paravartya"],
    answer:"Urdhva Tiryagbhyam" },

  { question:"Vedic Mathematics belongs to which country?",
    options:["India","China","Japan","Greece"],
    answer:"India" },

  { question:"Vedic methods reduce:",
    options:["Calculation time","Accuracy","Knowledge","Learning"],
    answer:"Calculation time" },

  { question:"Which technique helps in fast division?",
    options:["Paravartya Yojayet","Nikhilam","Urdhva","Ekadhikena"],
    answer:"Paravartya Yojayet" },

  { question:"Vedic Mathematics uses:",
    options:["Sutras and Sub-Sutras","Only calculators","Computer codes","Tables only"],
    answer:"Sutras and Sub-Sutras" },

  { question:"The number of Vedic Mathematics Sutras is:",
    options:["16","14","18","20"],
    answer:"16" },

  { question:"Which method is useful for multiplication of two digit numbers?",
    options:["Vertically Crosswise","Random method","Guess method","Graph method"],
    answer:"Vertically Crosswise" },

  { question:"Vedic Mathematics improves student's:",
    options:["Confidence in calculations","Internet speed","Hardware knowledge","Drawing"],
    answer:"Confidence in calculations" },

  { question:"Which Sutra uses the concept of previous number?",
    options:["Ekadhikena Purvena","Nikhilam","Paravartya","Yavadunam"],
    answer:"Ekadhikena Purvena" },

  // ---------- Part 2 (pehle comment ke andar chhupe hue the) ----------

  { question:"Which Vedic Sutra is used for simultaneous equations?",
    options:["Paravartya Yojayet","Nikhilam","Ekadhikena","Anurupyena"],
    answer:"Paravartya Yojayet" },

  { question:"Vedic Mathematics helps students develop:",
    options:["Mental ability","Only handwriting","Gaming skills","Drawing skills"],
    answer:"Mental ability" },

  { question:"Which operation is faster using Vedic techniques?",
    options:["Arithmetic calculations","Internet browsing","Programming","Typing"],
    answer:"Arithmetic calculations" },

  { question:"The base 10,100,1000 method is related to:",
    options:["Nikhilam Sutra","Division method","Addition method","Graph method"],
    answer:"Nikhilam Sutra" },

  { question:"Vedic Mathematics is useful for:",
    options:["Competitive exams","Only school writing","Computer repair","Hardware design"],
    answer:"Competitive exams" },

  { question:"Which Vedic Sutra is used for multiplication of numbers near a base?",
    options:["Nikhilam Navatashcaramam Dashatah","Paravartya Yojayet","Ekadhikena Purvena","Sunyam"],
    answer:"Nikhilam Navatashcaramam Dashatah" },

  { question:"The base method commonly uses bases like:",
    options:["10,100,1000","2,3,4","5,6,7","1,2,3"],
    answer:"10,100,1000" },

  { question:"Vedic Mathematics calculations are mainly:",
    options:["Mental","Mechanical","Computer based","Written only"],
    answer:"Mental" },

  { question:"Which Sutra is related to equations?",
    options:["Paravartya Yojayet","Nikhilam","Urdhva","Ekadhikena"],
    answer:"Paravartya Yojayet" },

  { question:"Vedic Mathematics was rediscovered by:",
    options:["Bharati Krishna Tirthaji","Aryabhata","Newton","Einstein"],
    answer:"Bharati Krishna Tirthaji" },

  { question:"The word Sutra means:",
    options:["Formula or Rule","Number","Calculation","Answer"],
    answer:"Formula or Rule" },

  { question:"Vedic Mathematics reduces:",
    options:["Calculation complexity","Knowledge","Memory","Practice"],
    answer:"Calculation complexity" },

  { question:"Which method is used for fast subtraction?",
    options:["Complement method","Graph method","Table method","Random method"],
    answer:"Complement method" },

  { question:"Vedic Mathematics is useful in:",
    options:["Competitive examinations","Only drawing","Only writing","Games"],
    answer:"Competitive examinations" },

  { question:"Which operation is called 'Vertically and Crosswise'?",
    options:["Multiplication","Division","Addition","Square root"],
    answer:"Multiplication" },

  { question:"Urdhva Tiryagbhyam is a:",
    options:["Multiplication Sutra","Division Sutra","Addition Sutra","Subtraction Sutra"],
    answer:"Multiplication Sutra" },

  { question:"Vedic Mathematics improves:",
    options:["Speed and accuracy","Only speed","Only memory","Only writing"],
    answer:"Speed and accuracy" },

  { question:"Which number system is used in Vedic Mathematics?",
    options:["Decimal","Binary","Roman","Hexadecimal"],
    answer:"Decimal" },

  { question:"A Sutra is a:",
    options:["Short mathematical principle","Computer program","Equation only","Number"],
    answer:"Short mathematical principle" },

  { question:"Vedic Mathematics techniques are:",
    options:["Simple and logical","Difficult","Random","Slow"],
    answer:"Simple and logical" },

  { question:"Which Sutra helps in finding squares quickly?",
    options:["Ekadhikena Purvena","Nikhilam","Paravartya","Sunyam"],
    answer:"Ekadhikena Purvena" },

  { question:"Vedic Mathematics mainly focuses on:",
    options:["Mental calculation","Drawing","Programming","Typing"],
    answer:"Mental calculation" },

  { question:"Fast multiplication saves:",
    options:["Time","Energy only","Memory","Numbers"],
    answer:"Time" },

  { question:"Vedic Mathematics techniques are based on:",
    options:["Ancient Indian mathematics","Modern physics","Computer science","Chemistry"],
    answer:"Ancient Indian mathematics" },

  { question:"The main advantage of Vedic Mathematics is:",
    options:["Quick calculation","Slow learning","Complex formulas","Long methods"],
    answer:"Quick calculation" }

];


// ================= VARIABLES =================

let currentQuestion = 0;
let selectedAnswers = [];
let score = 0;
let totalQuestions = questions.length;

// Ek flag taaki ek time pe ek hi save request chale
let isSaving = false;


// ================= SAVE ANSWER TO SERVER =================

function saveAnswerToServer(questionIndex, selectedOption, isCorrect) {

  isSaving = true;

  fetch("/submit_answer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      quiz_id: QUIZ_ID,
      question_index: questionIndex,
      selected_option: selectedOption,
      is_correct: isCorrect
    })
  })
  .then(res => res.json())
  .then(data => {
    isSaving = false;
    if (data.error) {
      console.error("Save answer error:", data.error);
    }
  })
  .catch(err => {
    isSaving = false;
    console.error("Network error while saving answer:", err);
  });

}


// ================= LOAD QUESTION =================

function loadQuestion(){

  let q = questions[currentQuestion];

  document.getElementById("questionNumber").innerHTML =
    "Question " + (currentQuestion + 1) + " / " + questions.length;

  document.getElementById("questionText").innerHTML = q.question;

  let optionsBox = document.getElementById("options");
  optionsBox.innerHTML = "";

  q.options.forEach((option, index) => {

    let div = document.createElement("div");
    div.className = "option-card";

    div.innerHTML = `
      <div class="option-letter">${String.fromCharCode(65 + index)}</div>
      <div class="option-text">${option}</div>
    `;

    // Agar is question ka answer pehle se select ho chuka hai
    // (Previous button se wapas aane par), to highlight karo
    if (selectedAnswers[currentQuestion] === option) {
      div.classList.add("selected");
    }

    div.onclick = function () {
      selectAnswer(option, div);
    };

    optionsBox.appendChild(div);

  });

  updateProgress();

}


// ================= SELECT ANSWER =================

function selectAnswer(answer, element){

  selectedAnswers[currentQuestion] = answer;

  let allOptions = document.querySelectorAll(".option-card");
  allOptions.forEach(item => item.classList.remove("selected"));

  element.classList.add("selected");

  let isCorrect = (answer === questions[currentQuestion].answer);

  // Turant server pe save karo (live persistence)
  saveAnswerToServer(currentQuestion, answer, isCorrect);

  updateProgress();

}


// ================= INITIAL LOAD =================

window.onload = function () {

  // Hero card + stat card ke "Total Questions" number ko
  // actual array length se set karo
  let heroTotal = document.getElementById("heroTotalQuestions");
  if (heroTotal) heroTotal.innerHTML = questions.length + " Questions";

  let statTotal = document.getElementById("totalQuestions");
  if (statTotal) statTotal.innerHTML = questions.length;

  let reviewTotal = document.getElementById("reviewTotal");
  if (reviewTotal) reviewTotal.innerHTML = questions.length;

  loadQuestion();

};


// ==================================================
// NAVIGATION FUNCTIONS
// ==================================================

function nextQuestion(){

  if (selectedAnswers[currentQuestion] == undefined) {
    alert("Please select an answer before continuing!");
    return;
  }

  if (currentQuestion < questions.length - 1) {
    currentQuestion++;
    loadQuestion();
  } else {
    document.getElementById("nextBtn").style.display = "none";
    document.getElementById("submitBtn").style.display = "block";
  }

}

function previousQuestion(){

  if (currentQuestion > 0) {
    currentQuestion--;
    loadQuestion();
  }

}


// ==================================================
// PROGRESS SYSTEM
// ==================================================

function updateProgress(){

  let attempted = selectedAnswers.filter(answer => answer !== undefined).length;
  let remaining = questions.length - attempted;
  let percentage = Math.round((attempted / questions.length) * 100);

  document.getElementById("attempted").innerHTML = attempted;
  document.getElementById("remaining").innerHTML = remaining;
  document.getElementById("completionStatus").innerHTML = percentage + "%";

  document.getElementById("progressBar").style.width = percentage + "%";
  document.getElementById("progressBar").innerHTML = percentage + "%";
  document.getElementById("progressText").innerHTML = percentage + "%";

  document.getElementById("prevBtn").disabled = (currentQuestion === 0);

  if (currentQuestion === questions.length - 1) {
    document.getElementById("nextBtn").style.display = "none";
    document.getElementById("submitBtn").style.display = "block";
  } else {
    document.getElementById("nextBtn").style.display = "block";
    document.getElementById("submitBtn").style.display = "none";
  }

}


// ==================================================
// SUBMIT QUIZ
// ==================================================

function submitQuiz(){

  let confirmSubmit = confirm("Are you sure you want to submit quiz?");

  if (confirmSubmit) {
    calculateResult();
  }

}


// ==================================================
// CALCULATE SCORE
// ==================================================

function calculateResult(){

  score = 0;

  questions.forEach((question, index) => {
    if (selectedAnswers[index] === question.answer) {
      score++;
    }
  });

  let percentage = Math.round((score / questions.length) * 100);

  document.querySelector(".question-card").style.display = "none";
  document.querySelector(".navigation").style.display = "none";

  let result = document.getElementById("resultBox");
  result.style.display = "block";

  document.getElementById("scoreCircle").innerHTML = percentage + "%";
  document.getElementById("scoreText").innerHTML = "Correct Answers : " + score;
  document.getElementById("percentageText").innerHTML = "Percentage : " + percentage + "%";

  let grade = "";

  if (percentage >= 90) grade = "Excellent 🏆";
  else if (percentage >= 75) grade = "Very Good ⭐";
  else if (percentage >= 50) grade = "Good 👍";
  else grade = "Need Improvement 📚";

  document.getElementById("gradeText").innerHTML = "Grade : " + grade;
  document.getElementById("messageText").innerHTML = getMessage(percentage);

}

function getMessage(per){

  if (per >= 90) return "Outstanding performance! You have mastered Vedic Mathematics 🎉";
  else if (per >= 70) return "Great job! Keep practicing more techniques ⭐";
  else if (per >= 50) return "Good effort! Practice more Sutras 📖";
  else return "Keep learning and improve your calculation skills 💪";

}


// ==================================================
// REVIEW SYSTEM
// ==================================================

function reviewAnswers(){

  let reviewBox = document.getElementById("reviewBox");
  reviewBox.style.display = "block";

  document.getElementById("resultBox").style.display = "none";

  let reviewContainer = document.getElementById("reviewQuestions");
  reviewContainer.innerHTML = "";

  let correct = 0;
  let wrong = 0;
  let attempted = 0;

  questions.forEach((question, index) => {

    let userAnswer = selectedAnswers[index];

    if (userAnswer !== undefined) attempted++;

    let statusClass = "";
    let statusText = "";

    if (userAnswer === question.answer) {
      correct++;
      statusClass = "correct-review";
      statusText = "✅ Correct Answer";
    } else {
      if (userAnswer !== undefined) wrong++;
      statusClass = "wrong-review";
      statusText = "❌ Wrong Answer";
    }

    let card = document.createElement("div");
    card.className = "review-card " + statusClass;

    card.innerHTML = `
      <h3>Question ${index + 1}</h3>
      <div class="review-question">${question.question}</div>
      <div class="answer-box">
        <p>Your Answer : <b>${userAnswer || "Not Attempted"}</b></p>
        <p>Correct Answer : <b>${question.answer}</b></p>
      </div>
      <div class="status">${statusText}</div>
    `;

    reviewContainer.appendChild(card);

  });

  document.getElementById("reviewTotal").innerHTML = questions.length;
  document.getElementById("reviewAttempt").innerHTML = attempted;
  document.getElementById("reviewCorrect").innerHTML = correct;
  document.getElementById("reviewWrong").innerHTML = wrong;

  let accuracy = 0;
  if (attempted > 0) accuracy = Math.round((correct / attempted) * 100);

  document.getElementById("reviewAccuracy").innerHTML = accuracy + "%";

}

function scrollToReview(){
  document.getElementById("reviewBox").scrollIntoView({ behavior: "smooth" });
}


// ==================================================
// DISABLE RIGHT CLICK (OPTIONAL)
// ==================================================

document.addEventListener("contextmenu", function (e) {
  e.preventDefault();
});


// ==================================================
// KEYBOARD NAVIGATION
// ==================================================

document.addEventListener("keydown", function (event) {
  if (event.key === "ArrowRight") nextQuestion();
  if (event.key === "ArrowLeft") previousQuestion();
});

// ==================================================
// END QUIZ SYSTEM
// ==================================================
