from app.database.connection import Database


class Comment:
    """Handles raw SQL operations for photo comments."""

    @staticmethod
    def create(photoId, userId, comment):
        """Create a new photo comment."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO comments (
                        photo_id,
                        user_id,
                        comment
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        photoId,
                        userId,
                        comment
                    )
                )

            connection.commit()

        finally:
            connection.close()

    @staticmethod
    def getByPhoto(photoId):
        """Return comments belonging to one photo."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        comments.id,
                        comments.photo_id,
                        comments.user_id,
                        comments.comment,
                        comments.date_time,
                        users.first_name,
                        users.last_name
                    FROM comments

                    INNER JOIN users
                        ON comments.user_id = users.id

                    WHERE comments.photo_id = %s

                    ORDER BY comments.date_time ASC
                    """,
                    (photoId,)
                )

                return cursor.fetchall()

        finally:
            connection.close()
