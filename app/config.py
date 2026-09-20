import os


class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "alzikrayat_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Alzikrayat12345")
    DB_NAME = os.getenv("DB_NAME", "alzikrayat")

#Alzikrayat12345