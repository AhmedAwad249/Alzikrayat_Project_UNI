const registerForm =
    document.getElementById("registerForm");


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        function (event) {

            const password =
                document.getElementById("password").value;

            const confirmPassword =
                document.getElementById("confirmPassword").value;

            if (password !== confirmPassword) {

                event.preventDefault();

                alert(
                    "Passwords do not match."
                );

            }

        }
    );

}


const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        function (event) {

            const email =
                document.getElementById("loginEmail").value.trim();

            const password =
                document.getElementById("loginPassword").value;

            if (!email || !password) {

                event.preventDefault();

                alert(
                    "Email and password are required."
                );

            }

        }
    );

}


const commentForms =
    document.querySelectorAll(
        ".commentForm"
    );

commentForms.forEach(function (form) {

    form.addEventListener(
        "submit",
        function (event) {

            const commentField =
                form.querySelector(
                    "textarea[name='comment']"
                );

            const comment =
                commentField.value.trim();

            if (!comment) {

                event.preventDefault();

                alert(
                    "Comment cannot be empty."
                );

            }

        }
    );

});