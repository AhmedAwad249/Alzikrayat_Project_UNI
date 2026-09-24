from flask import abort, redirect, render_template, session

from app.models.photo import Photo
from app.models.user import User


class UserController:
    """Shows member pages and their photos."""

    @staticmethod
    def index():
        """Show all registered members."""
        return render_template("users/index.html", users=User.getAll())

    @staticmethod
    def show(userId):
        """Show one member and their photos, or return 404 if missing."""
        user = User.findById(userId)

        if not user:
            abort(404)

        if session.get("userId") == userId:
            return redirect("/my-photos")

        photos = Photo.getByUser(userId)
        return render_template("users/show.html", user=user, photos=photos)
