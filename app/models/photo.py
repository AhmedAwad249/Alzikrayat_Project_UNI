from app.database.connection import Database


class Photo:
    """Handles raw SQL operations for photo records."""

    @staticmethod
    def create(
        userId,
        fileName,
        title,
        description=None
    ):
        """Create a new photo  ,return gene ID."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO photos (
                        user_id,
                        file_name,
                        title,
                        description
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        userId,
                        fileName,
                        title,
                        description
                    )
                )

                photoId = cursor.lastrowid

            connection.commit()

            return photoId

        finally:
            connection.close()

    @staticmethod
    def getAll():

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        photos.id,
                        photos.user_id,
                        photos.file_name,
                        photos.title,
                        photos.description,
                        photos.date_time,
                        users.first_name,
                        users.last_name
                    FROM photos

                    INNER JOIN users
                        ON photos.user_id = users.id

                    ORDER BY photos.date_time DESC
                    """
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def findById(photoId):

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        photos.id,
                        photos.user_id,
                        photos.file_name,
                        photos.title,
                        photos.description,
                        photos.date_time,
                        users.first_name,
                        users.last_name
                    FROM photos

                    INNER JOIN users
                        ON photos.user_id = users.id

                    WHERE photos.id = %s

                    LIMIT 1
                    """,
                    (photoId,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def getByUser(userId):
        """Return photos uploaded by a specific user."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        user_id,
                        file_name,
                        title,
                        description,
                        date_time
                    FROM photos

                    WHERE user_id = %s

                    ORDER BY date_time DESC
                    """,
                    (userId,)
                )

                return cursor.fetchall()

        finally:
            connection.close()

    @staticmethod
    def delete(photoId):

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM photos
                    WHERE id = %s
                    """,
                    (photoId,)
                )

            connection.commit()

        finally:
            connection.close()