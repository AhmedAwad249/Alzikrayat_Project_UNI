from datetime import datetime

from flask import (
    make_response,
    redirect,
    render_template,
    request,
    session
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.models.user import User
from app.validators.auth_validator import AuthValidator


class AuthController:
    """Handles registration, login, logout, and session state."""

    @staticmethod
    def showRegister():
        """Render the registration page."""

        if session.get("userId"):
            return redirect("/")

        return render_template(
            "auth/register.html",
            errors={},
            formData={}
        )

    @staticmethod
    def register():
        """Validate registration data and create a new user."""

        firstName = request.form.get("firstName", "").strip()
        lastName = request.form.get("lastName", "").strip()
        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")
        confirmPassword = request.form.get("confirmPassword", "")

        location = request.form.get("location", "").strip()
        occupation = request.form.get("occupation", "").strip()
        description = request.form.get("description", "").strip()

        errors = AuthValidator.validateRegistration(
            firstName,
            lastName,
            email,
            password,
            confirmPassword,
            location,
            occupation,
            description
        )

        if email and User.findByEmail(email):
            errors["email"] = "An account with this email already exists."

        formData = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "location": location,
            "occupation": occupation,
            "description": description
        }

        if errors:
            return render_template(
                "auth/register.html",
                errors=errors,
                formData=formData
            )

        passwordHash = generate_password_hash(
            password,
            method="pbkdf2:sha256"
        )

        User.create(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=passwordHash,
            location=location or None,
            occupation=occupation or None,
            description=description or None
        )

        return redirect("/login")

    @staticmethod
    def showLogin():
        """Render the login page + the last-login cookie."""

        if session.get("userId"):
            return redirect("/")

        lastLogin = request.cookies.get("lastLogin")

        return render_template(
            "auth/login.html",
            errors={},
            formData={},
            lastLogin=lastLogin
        )

    @staticmethod
    def login():
        """Authenticate a user and create a session."""

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        errors = AuthValidator.validateLogin(
            email,
            password
        )

        user = None

        if not errors:
            user = User.findByEmail(email)

            if not user or not check_password_hash( user["password"],password):
                errors["login"] = "Invalid email or password."

        if errors:
            return render_template(
                "auth/login.html",
                errors=errors,
                formData={
                    "email": email
                },
                lastLogin=request.cookies.get("lastLogin")
            )

        session.clear()

        session["userId"] = user["id"]
        session["firstName"] = user["first_name"]

        response = make_response(
            redirect("/")
        )

        currentLogin = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        response.set_cookie(
            "lastLogin",
            currentLogin,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            samesite="Lax"
        )

        return response

    @staticmethod
    def logout():
        """end the current authentication session."""

        session.clear()

        return redirect("/")