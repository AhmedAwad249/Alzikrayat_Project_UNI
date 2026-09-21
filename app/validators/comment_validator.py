class CommentValidator:
    """Validates photo comment."""

    @staticmethod
    def validate(comment):
        """Validate comment , return errors."""

        errors = {}

        if not comment:
            errors["comment"] = (
                "Comment cannot be empty."
            )

        elif len(comment) > 1000:
            errors["comment"] = (
                "Comment must not exceed 1000 characters."
            )

        return errors
