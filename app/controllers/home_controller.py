from flask import render_template

from app.models.user import User
from app.models.photo import Photo


class HomeController:
    """Handles requests for the home page."""

    @staticmethod
    def index():
        """Render the homepage."""

        userCount = User.count()
        photos = Photo.getAll()

        return render_template(
            "home.html",
            userCount=userCount,
            photoCount=len(photos),
            latestPhotos=photos[:3]
        )
