from flask import abort, redirect, session

from app.models.photo import Photo
from app.models.photo_like import PhotoLike


class LikeController:
    """Handles liking and unliking photos."""

    @staticmethod
    def toggle(photoId):
        """Toggle like on a photo."""

        if not session.get("userId"):
            return redirect("/login")

        photo = Photo.findById(photoId)

        if not photo:
            abort(404)

        userId = session["userId"]

        if PhotoLike.hasLiked( photoId ,userId):
            PhotoLike.remove(photoId ,userId)

        else:
            PhotoLike.add(photoId ,userId)

        return redirect(f"/photo/{photoId}")