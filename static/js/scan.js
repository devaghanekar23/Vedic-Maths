
alert("AI Lens JS Working");
const imageInput = document.getElementById("imageInput");

const preview = document.getElementById("preview");


if(imageInput){


    imageInput.addEventListener("change", function(){


        const file = this.files[0];


        if(file){


            const reader = new FileReader();



            reader.onload = function(e){


                preview.src = e.target.result;


                preview.style.display = "block";


            };



            reader.readAsDataURL(file);


        }


    });


}