import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'THIS IS A SECRET KEY'
    MONGO_URI = 'mongodb://localhost:27017/quiz_database'
