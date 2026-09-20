from flask import render_template

from app.models.user import User


class HomeController:
    """Handles requests for the home page."""

    @staticmethod
    def index():
        """Render the homepage."""

        userCount = User.count()

        return render_template(
            "home.html",
            userCount=userCount
        )