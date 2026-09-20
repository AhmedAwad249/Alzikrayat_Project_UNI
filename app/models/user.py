from app.database.connection import Database


class User:

    @staticmethod
    def count():
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