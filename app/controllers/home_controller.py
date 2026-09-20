from flask import render_template

from app.models.user import User


class HomeController:

    @staticmethod
    def index():
        userCount = User.count()

        return render_template(
            "home.html",
            userCount=userCount
        )