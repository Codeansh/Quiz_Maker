from quiz import mongo
# import ipdb;
#
# ipdb.set_trace()
quizes = mongo.db.Quizes


class Quizes():

    def __init__(self, title, current_user, description, questions, start, end, solvers, duration):

        self.title = title
        self.description = description
        quizes.insert_one(
            {'_id': title, 'maker': current_user, 'description': description, 'questions': questions, 'start': start,
             'end': end, 'solvers': solvers, 'duration': duration})

    @staticmethod
    def add_solvers(title, solvers):  # list of solvers
        qzs = quizes.find_one({'_id': title})
        l = qzs.get('solvers')
        if l:
            l.extend(solvers)
            l = list(set(l))
        else:
            l = list(set(solvers))
        quizes.update_one({'_id': title}, {'$set': {'solvers': l}})

    @staticmethod
    def add_questions(title, questions):  # dict containing ques-ans pair
        qzs = quizes.find_one({'_id': title})
        l = qzs.get('questions')
        l.update(questions)
        quizes.update_one({'_id': title}, {'$set': {'questions': l}})

    @staticmethod
    def update(title, description, questions, duration, solvers):
        qzs = quizes.find_one({'_id': title})
        quizes.update_one({'_id': title}, {
            '$set': {'description': description, 'questions': questions, 'duration': duration, 'solvers': solvers}})

    @staticmethod
    def find_by_maker(username):
        return list(quizes.find({'maker': username}))

    @staticmethod
    def find_quizes(_id):
        return quizes.find_one({'_id': _id})

    @staticmethod
    def is_active(title):
        qz = quizes.find_one({'_id': title})
        


    @staticmethod
    def remove_solvers(_id, l):
        qzs = quizes.find_one({'_id': _id})
        old = qzs.get('solvers')
        if not old:
            return "No solver present "
        l = list(set(old) - set(l))
        print(old, l)
        quizes.update_one({'_id': _id}, {'$set': {'solvers': l}})

    @staticmethod
    def delete(title):
        quizes.delete_one({'_id': title})

    @staticmethod
    def remove_questions(_id, l):
        qzs = quizes.find_one({'_id': _id})
        old = qzs.get('questions')
        if not old:
            return "No question present "
        for i in l:
            if i in old.keys():
                del old[i]
        quizes.update_one({'_id': _id}, {'$set': {'questions': old}})

    @staticmethod
    def get_all():
        qzs = list(quizes.find())
        return qzs
