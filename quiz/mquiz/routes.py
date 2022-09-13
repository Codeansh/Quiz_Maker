import json
from flask import Blueprint, request, jsonify
from quiz.authenticate import token_required
from quiz.mquiz.models import Quizzes
from quiz.mquiz.schemas import Create_Quiz, Update_quiz, Res_quiz
from quiz.mquiz.utilities import Quiz_to_dict
bp1 = Blueprint('mquiz', __name__,
                url_prefix='/makeq',
                template_folder='./templates')

@bp1.route('/create_new', methods=['POST'])
@token_required
def create_new(current_user):
    data = json.loads(request.data)
    data = Create_Quiz(**data).dict()
    data['maker'] = current_user.username
    quiz = Quizzes.create_quiz(data)
    quiz = Res_quiz(**Quiz_to_dict(quiz)).dict()
    return jsonify(quiz)


@bp1.route('/update_quiz/<title>', methods=['GET', 'POST'])
@token_required
def update(current_user, title):
    quiz = Quizzes.objects(title=title).first()
    if not quiz:
        return 'Quiz Not Found'
    if quiz.maker != current_user.username:
        return {'alert': 'Not allowed to update'}
    data = json.loads(request.data)
    data = Update_quiz(**data).dict()

    quiz = quiz.update(**data)
    quiz = Quizzes.objects(title=title).first()

    return jsonify(quiz)


@bp1.route('view_quizes')
@token_required
def view_quizes(current_user):
    qzs = Quizzes.objects(maker=current_user.username)
    return jsonify(qzs)


@bp1.route('delete_quiz/<title>', methods=['GET'])
@token_required
def delete_quiz(current_user, title):
    qzs = Quizzes.objects(title=title).first()
    if not qzs:
        return {'failed': 'quiz not found'}
    if qzs.maker != current_user.username:
        return {'alert': 'Not allowed to delete'}

    qzs.delete()

    return {'success': 'Deleted successfully'}


@bp1.route('/add_solvers/<title>', methods=['GET', 'POST'])
@token_required
def add_solvers(current_user, title:str):
    quiz = Quizzes.objects(title=title).first()
    if not quiz:
        return {'message': 'Quiz Not Found'}

    if not quiz.maker != current_user.username:
        return {'Alert': 'Action not allowed '}

    solvers = json.loads(request.data)['solvers']
    old_solvers = quiz.solvers

    old_solvers.update(solvers)
    qzs = quiz.update(solvers = old_solvers)
    qzs = Quizzes.objects(title=title)
    return {'Solvers Added': qzs}

