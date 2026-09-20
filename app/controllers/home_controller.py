from flask import render_template


class HomeController:

    @staticmethod
    def index():
        return render_template("home.html")