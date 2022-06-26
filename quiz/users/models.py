from werkzeug.security import generate_password_hash, check_password_hash

from quiz.database import user, quizes


class User():
    def __init__(self, username, fullname, email):
        self.username = username
        self.name = fullname
        self.email = email
        user.insert_one({'_id': username, 'fullname': fullname, 'email': email, 'password': None})

    def set_password(self, password):
        u = user.update_one({'_id': self.username}, {'$set': {'password': generate_password_hash(password)}})

    def check_password(self, password):
        p = user.find_one({'_id': self.username}).get('password')
        return check_password_hash(p, password)

    @staticmethod
    def get_user(username):
        return user.find_one({'_id': username})

    @staticmethod
    def check_password(username, password):
        p = user.find_one({'_id': username}).get('password')
        return check_password_hash(p, password)

    @staticmethod
    def get_all_quizes(username):
        qzs = list(quizes.find({'solvers': {'$in': [username]}}))
        return qzs
