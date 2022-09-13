
# import ipdb;
# ipdb.set_trace()
from quiz.users.models import User
from mongoengine import Document, StringField, IntField, ReferenceField,EmailField,DictField


class Quizzes(Document):
    title = StringField(required=True)
    maker =  StringField()
    questions = DictField()
    description = StringField()
    duration = IntField()
    solvers = DictField()

    @staticmethod
    def create_quiz(data):
        quiz = Quizzes(**data).save()
        return quiz

    @staticmethod
    def find_quiz(title):
        quiz = Quizzes(title=title)
        return quiz


