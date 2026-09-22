import os
import uuid

from flask import (
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session
)


from werkzeug.utils import secure_filename

from app.models.comment import Comment
from app.models.photo import Photo
from app.models.user import User
from app.models.photo_tag import PhotoTag
from app.validators.photo_validator import PhotoValidator
from app.models.photo_like import PhotoLike


class PhotoController:
    """Handles photo gallery, upload, details, deletion."""

    @staticmethod
    def index():
        """Display all uploaded photos."""

        photos = Photo.getAll()

        return render_template(
            "photos/index.html",
            photos=photos
        )

    @staticmethod
    def show(photoId):
        """Display one photo, comments, likes, and tagged users."""

        photo = Photo.findById(photoId)

        if not photo:
            abort(404)

        comments = Comment.getByPhoto(photoId)

        likeCount = PhotoLike.countByPhoto(photoId)

        likedByCurrentUser = False

        if session.get("userId"):
            likedByCurrentUser = (
                PhotoLike.hasLiked(photoId ,session["userId"])
            )

        taggedUsers = (PhotoTag.getUsersForPhoto(photoId))

        return render_template(
            "photos/show.html",
            photo=photo,
            comments=comments,
            commentErrors={},
            likeCount=likeCount,
            likedByCurrentUser=likedByCurrentUser,
            taggedUsers=taggedUsers
        )

    @staticmethod
    def showUpload():
        """Display photo upload form."""

        if not session.get("userId"):
            return redirect("/login")

        users = User.getAllExcept(session["userId"])

        return render_template(
            "photos/create.html",
            errors={},
            formData={},
            users=users
        )

    @staticmethod
    def store():
        """Validate, save, and store an uploaded photo."""

        if not session.get("userId"):
            return redirect("/login")

        photoFile = request.files.get("photo")
        title = request.form.get(
            "title",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()
        

        errors = PhotoValidator.validateUpload(
            photoFile,
            title,
            description
        )

        if errors:
            users = User.getAllExcept(session["userId"])
            return render_template(
                "photos/create.html",
                errors=errors,
                formData={
                    "title": title,
                    "description": description},
                    users=users
            )

        originalName = secure_filename(
            photoFile.filename
        )

        extension = originalName.rsplit(
            ".",
            1
        )[1].lower()

        fileName = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        uploadDirectory = os.path.join(
            current_app.static_folder,
            "uploads"
        )

        os.makedirs(
            uploadDirectory,
            exist_ok=True
        )

        filePath = os.path.join(
            uploadDirectory,
            fileName
        )

        photoFile.save(filePath)

        photoId = Photo.create(
            userId=session["userId"],
            fileName=fileName,
            title=title,
            description=description or None
        )

        allowedUsers = User.getAllExcept(session["userId"])
        allowedUserIds = {str(user["id"])for user in allowedUsers}

        taggedUsers = request.form.getlist("taggedUsers")

        for taggedUserId in taggedUsers:

            if taggedUserId not in allowedUserIds:
                continue

            PhotoTag.add( photoId=photoId ,userId=int(taggedUserId) )

        return redirect("/photos")

    @staticmethod
    def myPhotos():
        """Display photos for logged-in user."""

        if not session.get("userId"):
            return redirect("/login")

        photos = Photo.getByUser(session["userId"])

        return render_template("photos/my_photos.html",photos=photos)

    @staticmethod
    def delete(photoId):
        """Delete a photo only when owned by the current user."""

        if not session.get("userId"):
            return redirect("/login")

        photo = Photo.findById(photoId)

        if not photo:
            abort(404)

        if photo["user_id"] != session["userId"]:
            abort(403)

        filePath = os.path.join(
            current_app.static_folder,
            "uploads",
            photo["file_name"]
        )

        Photo.delete(photoId)

        if os.path.exists(filePath):
            os.remove(filePath)

        return redirect("/my-photos")