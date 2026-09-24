from flask import (
    abort,
    redirect,
    render_template,
    request,
    session
)

from app.models.comment import Comment
from app.models.photo import Photo
from app.models.photo_like import PhotoLike
from app.models.photo_tag import PhotoTag
from app.validators.comment_validator import CommentValidator


class CommentController:
    """Handles creation of photo comments."""

    @staticmethod
    def store(photoId):
        """Validate and store a new comment."""

        if not session.get("userId"):
            return redirect("/login")

        photo = Photo.findById(photoId)

        if not photo:
            abort(404)

        commentText = request.form.get(
            "comment",
            ""
        ).strip()

        errors = CommentValidator.validate(commentText)

        if errors:
            comments = Comment.getByPhoto(photoId)

            return render_template(
                "photos/show.html",
                photo=photo,
                comments=comments,
                commentErrors=errors,
                likeCount=PhotoLike.countByPhoto(photoId),
                likedByCurrentUser=PhotoLike.hasLiked(photoId, session["userId"]),
                taggedUsers=PhotoTag.getUsersForPhoto(photoId)
            ), 400

        Comment.create(
            photoId=photoId,
            userId=session["userId"],
            comment=commentText
        )

        return redirect(
            f"/photo/{photoId}#comments"
        )
