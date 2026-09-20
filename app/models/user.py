from app.database.connection import Database


class User:
    """ raw SQL operations for user records."""

    @staticmethod
    def count():
        """total number of registered users."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) AS total FROM users"
                )

                result = cursor.fetchone()

                return result["total"]

        finally:
            connection.close()

    @staticmethod
    def findById(userId):
        """Find a user by numeric ID."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        first_name,
                        last_name,
                        email,
                        location,
                        occupation,
                        description
                    FROM users
                    WHERE id = %s
                    LIMIT 1
                    """,
                    (userId,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def findByEmail(email):
        """Find a user by email address."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        first_name,
                        last_name,
                        email,
                        password,
                        location,
                        occupation,
                        description
                    FROM users
                    WHERE email = %s
                    LIMIT 1
                    """,
                    (email,)
                )

                return cursor.fetchone()

        finally:
            connection.close()

    @staticmethod
    def create(
        firstName,
        lastName,
        email,
        password,
        location=None,
        occupation=None,
        description=None
    ):
        """Create a new user and return the generated ID."""

        connection = Database.getConnection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (
                        first_name,
                        last_name,
                        email,
                        password,
                        location,
                        occupation,
                        description
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        firstName,
                        lastName,
                        email,
                        password,
                        location,
                        occupation,
                        description
                    )
                )

                userId = cursor.lastrowid

            connection.commit()

            return userId

        finally:
            connection.close()