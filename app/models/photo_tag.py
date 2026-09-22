from app.database.connection import Database


class PhotoTag:
    """Handles user tags -> photos."""

    @staticmethod
    def add(photoId, userId):

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT IGNORE INTO photo_tags (
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
    def getUsersForPhoto(photoId):
        """Return registered users tagged in a photo."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        users.id,
                        users.first_name,
                        users.last_name
                    FROM photo_tags

                    INNER JOIN users
                        ON photo_tags.user_id = users.id

                    WHERE photo_tags.photo_id = %s

                    ORDER BY users.first_name ASC
                    """,
                    (photoId,)
                )

                return cursor.fetchall()

        finally:
            connection.close()