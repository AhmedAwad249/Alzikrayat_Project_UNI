import re


class AuthValidator:
    """Validates authentication form data."""

    @staticmethod
    def validateRegistration(
        firstName,
        lastName,
        email,
        password,
        confirmPassword,
        location="",
        occupation="",
        description=""
    ):

        """Validate registration fields and return validation errors."""
        errors = {}

        if not firstName:
            errors["firstName"] = "First name is required."
        elif len(firstName) > 50:
            errors["firstName"] = "First name must not exceed 50 characters."
        elif not firstName.isalpha():
            errors["firstName"] = "First name must contain letters only."

        if not lastName:
            errors["lastName"] = "Last name is required."
        elif len(lastName) > 50:
            errors["lastName"] = "Last name must not exceed 50 characters."
        elif not lastName.isalpha():
            errors["lastName"] = "Last name must contain letters only."

        emailPattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not email:
            errors["email"] = "Email is required."
        elif len(email) > 100:
            errors["email"] = "Email must not exceed 100 characters."
        elif not re.match(emailPattern, email):
            errors["email"] = "Enter a valid email address."

        if not password:
            errors["password"] = "Password is required."
        elif len(password) < 8:
            errors["password"] = "Password must contain at least 8 characters."

        if password != confirmPassword:
            errors["confirmPassword"] = "Passwords do not match."

        if len(location) > 100:
            errors["location"] = "Location must not exceed 100 characters."

        if len(occupation) > 100:
            errors["occupation"] = "Occupation must not exceed 100 characters."

        if len(description) > 1000:
            errors["description"] = "Description is too long."

        return errors

    @staticmethod
    def validateLogin(email, password):
        """Validate login fields and return validation errors."""

        errors = {}

        if not email:
            errors["email"] = "Email is required."

        if not password:
            errors["password"] = "Password is required."

        return errors