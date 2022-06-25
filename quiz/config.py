import os 

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'THIS IS A SECRET KEY'