from app.database.connection import Database


class PhotoLike:
    """Handles raw SQL operations for photo likes."""

    @staticmethod
    def hasLiked(photoId, userId):
        """user already liked a photo ? """

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM photo_likes
                    WHERE photo_id = %s
                    AND user_id = %s
                    LIMIT 1
                    """,
                    (
                        photoId,
                        userId
                    )
                )

                return cursor.fetchone() is not None

        finally:
            connection.close()

    @staticmethod
    def add(photoId, userId):
        """Add a like to a photo."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO photo_likes (
                        photo_id,
                        user_id
                    )
                    VALUES (%s, %s)
                    """,
                    (
                        photoId,
                        userId
                    )
                )

            connection.commit()

        finally:
            connection.close()

    @staticmethod
    def remove(photoId, userId):
        """Remove a user's like from a photo."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM photo_likes
                    WHERE photo_id = %s
                    AND user_id = %s
                    """,
                    (
                        photoId,
                        userId
                    )
                )

            connection.commit()

        finally:
            connection.close()

    @staticmethod
    def countByPhoto(photoId):
        """Return the number of likes on a photo."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*) AS total
                    FROM photo_likes
                    WHERE photo_id = %s
                    """,
                    (photoId,)
                )

                result = cursor.fetchone()

                return result["total"]

        finally:
            connection.close()