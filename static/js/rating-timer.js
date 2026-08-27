document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       SETTINGS
    ========================================================= */

    const RATING_TIME = 5 * 60 * 1000; // 5 minutes


    /* =========================================================
       FIND RATING MODAL
    ========================================================= */

    const overlay =
        document.getElementById("ratingOverlay");

    const stars =
        document.querySelectorAll(".modal-star");

    const submitBtn =
        document.getElementById("modalSubmitRating");

    const ratingText =
        document.getElementById("modalRatingText");


    // If rating modal doesn't exist on this page
    if (!overlay) {
        return;
    }


    let selectedRating = 0;


    /* =========================================================
       RATING MESSAGES
    ========================================================= */

    const ratingMessages = {
        1: "Poor 😞",
        2: "Could be better 😕",
        3: "Good 🙂",
        4: "Very Good 😊",
        5: "Excellent! 🤩"
    };


    /* =========================================================
       POPUP INITIALLY HIDDEN
    ========================================================= */

    overlay.style.display = "none";


    /* =========================================================
       CHECK WHETHER USER ALREADY RATED
    ========================================================= */

    fetch("/get-user-rating")
        .then(response => response.json())
        .then(data => {

            /* -------------------------------------------------
               USER ALREADY RATED
            ------------------------------------------------- */

            if (data.hasRated) {

                // Remove old timer
                localStorage.removeItem("appStartTime");

                // Don't show popup
                overlay.style.display = "none";

                return;
            }


            /* -------------------------------------------------
               USER HAS NOT RATED
            ------------------------------------------------- */

            startRatingTimer();

        })
        .catch(error => {

            console.error(
                "Rating check error:",
                error
            );

        });


/* =========================================================
   START / CONTINUE 5 MINUTE TIMER
========================================================= */

function startRatingTimer() {

    // AGAR NAYA LOGIN HAI TO PURANA TIMER RESET KAREIN (Fix for Instant Popup)
    if (document.referrer.includes('google') || !sessionStorage.getItem("sessionActive")) {
        localStorage.removeItem("appStartTime");
        sessionStorage.setItem("sessionActive", "true");
    }

    let startTime = localStorage.getItem("appStartTime");


    /* -------------------------------------------------
        FIRST TIME
    ------------------------------------------------- */

    if (!startTime) {

        startTime = Date.now();

        localStorage.setItem(
            "appStartTime",
            startTime
        );

        console.log(
            "Rating timer started fresh."
        );
    }

    /* -------------------------------------------------
        CALCULATE ELAPSED TIME
    ------------------------------------------------- */

    const elapsedTime =
        Date.now() - parseInt(startTime);


    /* -------------------------------------------------
        CALCULATE REMAINING TIME
    ------------------------------------------------- */

    const remainingTime =
        RATING_TIME - elapsedTime;


    console.log(
        "Rating timer remaining:",
        Math.max(
            0,
            Math.ceil(
                remainingTime / 1000
            )
        ),
        "seconds"
    );


    /* -------------------------------------------------
        5 MINUTES ALREADY COMPLETED
    ------------------------------------------------- */

    if (remainingTime <= 0) {

        showRatingPopup();

        return;
    }


    /* -------------------------------------------------
        WAIT UNTIL 5 MINUTES COMPLETE
    ------------------------------------------------- */

    setTimeout(function () {

        showRatingPopup();

    }, remainingTime);

}


    /* =========================================================
       SHOW RATING POPUP
    ========================================================= */

    function showRatingPopup() {

        overlay.style.display = "flex";

        console.log(
            "7 minutes completed. Rating popup opened."
        );

    }


    /* =========================================================
       STAR SELECTION
    ========================================================= */

    stars.forEach(star => {

        star.addEventListener(
            "click",
            function () {

                selectedRating =
                    parseInt(
                        this.getAttribute(
                            "data-value"
                        )
                    );


                /* ---------------------------------------------
                   UPDATE STAR DISPLAY
                --------------------------------------------- */

                updateStars(
                    selectedRating
                );


                /* ---------------------------------------------
                   ENABLE SUBMIT BUTTON
                --------------------------------------------- */

                submitBtn.disabled = false;


                /* ---------------------------------------------
                   SHOW MESSAGE
                --------------------------------------------- */

                ratingText.textContent =
                    ratingMessages[
                        selectedRating
                    ];

            }
        );

    });


    /* =========================================================
       UPDATE STARS
    ========================================================= */

    function updateStars(rating) {

        stars.forEach(star => {

            const value =
                parseInt(
                    star.getAttribute(
                        "data-value"
                    )
                );


            if (value <= rating) {

                star.classList.add(
                    "selected"
                );

                star.textContent = "★";

            } else {

                star.classList.remove(
                    "selected"
                );

                star.textContent = "☆";

            }

        });

    }


    /* =========================================================
       SUBMIT RATING
    ========================================================= */

    submitBtn.addEventListener(
        "click",
        function () {

            /* ---------------------------------------------
               NO RATING SELECTED
            --------------------------------------------- */

            if (selectedRating === 0) {

                return;
            }


            /* ---------------------------------------------
               DISABLE BUTTON
            --------------------------------------------- */

            submitBtn.disabled = true;

            submitBtn.textContent =
                "Submitting...";


            /* ---------------------------------------------
               SEND RATING TO FLASK
            --------------------------------------------- */

            fetch(
                "/submit-rating",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        rating:
                            selectedRating
                    })
                }
            )
            .then(response =>
                response.json()
            )
            .then(data => {


                /* -----------------------------------------
                   SUCCESS
                ----------------------------------------- */

                if (data.success) {

                    ratingText.textContent =
                        "Thank you for your feedback! ❤️";


                    submitBtn.textContent =
                        "Thank You ❤️";


                    /* -------------------------------------
                       IMPORTANT

                       Remove timer because user
                       has already rated.
                    ------------------------------------- */

                    localStorage.removeItem(
                        "appStartTime"
                    );


                    /* -------------------------------------
                       CLOSE POPUP
                    ------------------------------------- */

                    setTimeout(
                        function () {

                            overlay.style.display =
                                "none";

                        },
                        1000
                    );


                } else {


                    /* -----------------------------------------
                       ERROR
                    ----------------------------------------- */

                    alert(
                        data.message ||
                        "Unable to submit rating."
                    );


                    submitBtn.disabled =
                        false;


                    submitBtn.textContent =
                        "Submit Rating";

                }

            })
            .catch(error => {

                console.error(
                    "Rating submit error:",
                    error
                );


                alert(
                    "Something went wrong. Please try again."
                );


                submitBtn.disabled =
                    false;


                submitBtn.textContent =
                    "Submit Rating";

            });

        }
    );
    /* ==========================================
   CLEAR TIMER WHEN USER LOGS OUT
========================================== */

const logoutLinks = document.querySelectorAll(
    'a[href*="/logout"]'
);

logoutLinks.forEach(link => {

    link.addEventListener("click", function () {

        localStorage.removeItem("appStartTime");

        console.log(
            "Rating timer cleared because user logged out."
        );

    });

});

});