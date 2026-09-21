class PhotoValidator:
    """Validates photo upload form data."""

    ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }

    @staticmethod
    def validateUpload(photoFile, title, description):
        """Validate metadata."""

        errors = {}

        if not photoFile or not photoFile.filename:
            errors["photo"] = "Please select an image."

        elif not PhotoValidator.isAllowedFile(
            photoFile.filename
        ):
            errors["photo"] = (
                "Only JPG, JPEG, PNG, and WEBP files are allowed."
            )

        if not title:
            errors["title"] = "Photo title is required."

        elif len(title) > 200:
            errors["title"] = (
                "Photo title must not exceed 200 characters."
            )

        if len(description) > 2000:
            errors["description"] = (
                "Description is too long."
            )

        return errors

    @staticmethod
    def isAllowedFile(fileName):
        """Check file extension is allowed."""

        if "." not in fileName:
            return False

        extension = fileName.rsplit(".", 1)[1].lower()

        return extension in PhotoValidator.ALLOWED_EXTENSIONS