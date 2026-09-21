import pymysql

from app.config import Config


class Database:

    @staticmethod
    def getConnection():
        connection = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
        with connection.cursor() as cursor:
            cursor.execute("SET time_zone = '+00:00'")

        return connection